"""
Eval for the Vendor Sales SQL Agent.

Part A: guardrail tests (validator + AST calculator) -> "did the guardrail block it?"
Part B: end-to-end agent eval on a golden question set -> "is the agent's answer correct?"

HOW TO USE
1. Part A runs as-is:   python eval_sql_agent_v2.py
2. For Part B, fill in the 3 TODOs below (DB path, ask_agent, GOLDEN questions).
"""
import ast
import json
import operator
import re
import sqlite3
import time

# ----------------------------------------------------------------------------
# Part A -- guardrails
# TODO (optional): replace these two functions with imports from your agent file,
# e.g.  from agent_sql_v2 import is_safe_sql, safe_calculate
# so the eval tests the REAL code and not a copy.
# ----------------------------------------------------------------------------
FORBIDDEN = {
    "DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "ATTACH", "DETACH",
    "PRAGMA", "CREATE", "VACUUM", "REINDEX", "LOAD_EXTENSION",
}


def is_safe_sql(query: str) -> bool:
    q = re.sub(r"--[^\n]*", " ", query)               # strip line comments
    q = re.sub(r"/\*.*?\*/", " ", q, flags=re.S)       # strip block comments
    q = q.strip().rstrip(";").strip()
    if ";" in q:                                       # no multi-statement input
        return False
    up = q.upper()
    if not up.startswith("SELECT"):
        return False
    tokens = set(re.findall(r"[A-Z_]+", up))           # catches ';DROP' with no space
    return not (tokens & FORBIDDEN)


_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv}


def safe_calculate(expr: str):
    node = ast.parse(expr, mode="eval").body

    def _eval(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)) and not isinstance(n.value, bool):
            return n.value
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, ast.USub):   # negative numbers (e.g. negative margin)
            return -_eval(n.operand)
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](_eval(n.left), _eval(n.right))
        raise ValueError("Unsafe expression")

    return _eval(node)


# (query, should_be_allowed)
SQL_CASES = [
    # valid read queries
    ("SELECT vendor_name, SUM(sales) FROM sales GROUP BY vendor_name LIMIT 5;", True),
    ("SELECT COUNT(*) FROM purchases WHERE purchase_date >= '2024-01-01';", True),
    ("SELECT brand, AVG(margin) FROM vendor_summary GROUP BY brand HAVING COUNT(*) > 10;", True),
    ("SELECT * FROM inventory WHERE stock < 50;", True),
    ("SELECT a.vendor_id, b.total FROM vendors a JOIN sales b ON a.id = b.vendor_id;", True),
    ("select update_date, delete_flag from sales", True),                       # keyword-looking column names
    ("SELECT * FROM sales -- latest rows\nLIMIT 10", True),                     # harmless comment
    # destructive statements
    ("DROP TABLE sales;", False),
    ("DELETE FROM vendors WHERE id = 1;", False),
    ("UPDATE sales SET profit = 999999;", False),
    ("INSERT INTO vendors VALUES (999, 'Hack');", False),
    ("ALTER TABLE sales ADD COLUMN x INT;", False),
    ("PRAGMA writable_schema = 1;", False),
    ("ATTACH DATABASE 'other.db' AS o;", False),
    # sneaky injection / multi-statement
    ("SELECT * FROM sales; DROP TABLE sales;", False),
    ("SELECT * FROM sales;DROP TABLE sales;", False),                           # no space after ;
    ("SELECT * FROM sales;\nDELETE FROM sales", False),                         # newline
    ("SELECT * FROM sales; /* hi */ DELETE FROM sales;", False),                # comment between
    ("select * from sales; drop table sales;", False),                          # lowercase
    ("WITH x AS (SELECT 1) DELETE FROM sales;", False),                         # CTE write
    ("SELECT load_extension('evil.so');", False),
]

MATH_CASES = [
    ("(45000 - 30000) / 45000", True),
    ("-5 + 3", True),
    ("(1 + 2) * 3", True),
    ("__import__('os').system('dir')", False),
    ("open('secret.db').read()", False),
    ("2 ** 99999999", False),                  # power not allowed (DoS)
    ("[x for x in range(10**9)]", False),
    ("'a' * 10", False),
]


def run_guardrail_eval():
    sql_fail = [(q, exp) for q, exp in SQL_CASES if is_safe_sql(q) != exp]
    math_fail = []
    for expr, should_pass in MATH_CASES:
        try:
            safe_calculate(expr)
            ok = should_pass
        except Exception:
            ok = not should_pass
        if not ok:
            math_fail.append(expr)

    adv_sql = [c for c in SQL_CASES if c[1] is False]
    adv_blocked = sum(1 for q, _ in adv_sql if not is_safe_sql(q))
    print("=== Part A: Guardrails ===")
    print(f"SQL validator   : {len(SQL_CASES) - len(sql_fail)}/{len(SQL_CASES)} correct "
          f"| adversarial blocked: {adv_blocked}/{len(adv_sql)}")
    print(f"AST calculator  : {len(MATH_CASES) - len(math_fail)}/{len(MATH_CASES)} correct")
    for q, exp in sql_fail:
        print(f"  FAIL sql  (expected allowed={exp}): {q!r}")
    for e in math_fail:
        print(f"  FAIL math: {e!r}")
    return sql_fail, math_fail


# ----------------------------------------------------------------------------
# Part B -- end-to-end agent eval (execution accuracy)
# Idea: for each question, run your agent, take the SQL it finally ran, execute it,
# and compare the rows with the rows of a gold SQL that YOU wrote and checked by hand.
# This is robust to the agent writing different-but-equivalent SQL.
# ----------------------------------------------------------------------------
import os
import time

import agent_sql as base
import agent_sql_v2 as v2
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from golden_cases import GOLDEN

load_dotenv()
DB_PATH = base.DB_PATH
_llm = ChatGoogleGenerativeAI(model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"), temperature=0)
_app = v2.build_graph(_llm)


def ask_agent(question: str) -> dict:
    last_err = None
    for attempt in range(3):                      # retry transient API errors (429/503)
        try:
            r = v2.ask(_app, question)
            return {"final_sql": r.last_sql, "steps": r.steps,
                    "sql_errors": r.sql_errors, "answer": r.answer}
        except Exception as e:
            last_err = e
            time.sleep(10 * (attempt + 1))
    raise last_err
def _norm(rows, ordered):
    rows = [tuple(v.strip() if isinstance(v, str) else (round(v, 2) if isinstance(v, float) else v) for v in r) for r in rows]
    return rows if ordered else sorted(rows, key=repr)


def _run(conn, sql):
    return conn.execute(sql).fetchall()


def run_agent_eval():
    if not GOLDEN:
        print("\n=== Part B: skipped (GOLDEN is empty) ===")
        return None
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    results = []
    for case in GOLDEN:
        t0 = time.time()
        rec = {"question": case["q"], "correct": False, "steps": None, "sql_errors": None, "latency_s": None, "error": None}
        try:
            out = ask_agent(case["q"])
            rec["latency_s"] = round(time.time() - t0, 2)
            rec["steps"], rec["sql_errors"] = out.get("steps"), out.get("sql_errors")
            ordered = "ORDER BY" in case["gold_sql"].upper()
            gold = _norm(_run(conn, case["gold_sql"]), ordered)
            got = _norm(_run(conn, out["final_sql"]), ordered) if out.get("final_sql") else None
            rec["correct"] = got == gold
        except NotImplementedError:
            print("\n=== Part B: fill in ask_agent() first ===")
            return None
        except Exception as e:                      # agent crashed / bad SQL counts as wrong
            rec["error"] = str(e)
        results.append(rec)
        print(("PASS " if rec["correct"] else "FAIL ") + case["q"])

    n = len(results)
    ok = sum(r["correct"] for r in results)
    lat = [r["latency_s"] for r in results if r["latency_s"] is not None]
    stp = [r["steps"] for r in results if r["steps"] is not None]
    print("\n=== Part B: Agent eval ===")
    print(f"Execution accuracy : {ok}/{n} ({ok / n * 100:.0f}%)")
    if stp:
        print(f"Avg LLM steps      : {sum(stp) / len(stp):.1f}")
    if lat:
        print(f"Avg latency        : {sum(lat) / len(lat):.1f} s")
    print(f"Total SQL errors   : {sum(r['sql_errors'] or 0 for r in results)}")
    with open("eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved eval_results.json (keep this -- it is your evidence)")
    return results


if __name__ == "__main__":
    run_guardrail_eval()
    run_agent_eval()