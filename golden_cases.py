"""
Golden questions for the Vendor Sales SQL Agent eval.
Each case: a question + the correct SQL (gold). The eval runs the gold SQL and the
agent's final SQL on the same DB and compares the rows.

IMPORTANT before you trust these:
1. Run check_gold() at the bottom once and look at the rows -- confirm by eye that each
   result is sane (right magnitude, no NULL/None surprises). Fix or drop any case that looks off.
2. The question wording says exactly which columns to return, so a correct agent
   returns the same columns as the gold SQL.
"""

GOLDEN = [
    # --- simple aggregates ---
    {"q": "How many rows are in the sales table? Return a single number.",
     "gold_sql": "SELECT COUNT(*) FROM sales"},
    {"q": "What is the total SalesDollars across the whole sales table? Return a single number.",
     "gold_sql": "SELECT SUM(SalesDollars) FROM sales"},
    {"q": "What is the total Freight in the vendor_invoice table? Return a single number.",
     "gold_sql": "SELECT SUM(Freight) FROM vendor_invoice"},
    {"q": "What is the total onHand quantity in the end_inventory table? Return a single number.",
     "gold_sql": "SELECT SUM(onHand) FROM end_inventory"},
    {"q": "How many distinct vendors (VendorNumber) are in final_summary? Return a single number.",
     "gold_sql": "SELECT COUNT(DISTINCT VendorNumber) FROM final_summary"},
    {"q": "How many rows in final_summary have a negative GrossProfit? Return a single number.",
     "gold_sql": "SELECT COUNT(*) FROM final_summary WHERE GrossProfit < 0"},
    {"q": "What is the average PurchasePrice in the purchase_prices table, rounded to 2 decimals? Return a single number.",
     "gold_sql": "SELECT ROUND(AVG(PurchasePrice), 2) FROM purchase_prices"},

    # --- group by / top-N ---
    {"q": "Which 5 vendors have the highest total purchase Dollars in the purchases table? Return VendorName and the total.",
     "gold_sql": "SELECT VendorName, SUM(Dollars) FROM purchases GROUP BY VendorName ORDER BY SUM(Dollars) DESC LIMIT 5"},
    {"q": "Which 5 brands have the highest GrossProfit in final_summary? Return Brand and GrossProfit.",
     "gold_sql": "SELECT Brand, GrossProfit FROM final_summary ORDER BY GrossProfit DESC LIMIT 5"},
    {"q": "Which 3 stores have the highest total SalesDollars in the sales table? Return Store and the total.",
     "gold_sql": "SELECT Store, SUM(SalesDollars) FROM sales GROUP BY Store ORDER BY SUM(SalesDollars) DESC LIMIT 3"},
    {"q": "Which vendor sold the most units in the sales table? Return VendorName and total SalesQuantity.",
     "gold_sql": "SELECT VendorName, SUM(SalesQuantity) FROM sales GROUP BY VendorName ORDER BY SUM(SalesQuantity) DESC LIMIT 1"},
    {"q": "Which vendor has the highest total Freight in the vendor_invoice table? Return VendorNumber and the total Freight.",
     "gold_sql": "SELECT VendorNumber, SUM(Freight) FROM vendor_invoice GROUP BY VendorNumber ORDER BY SUM(Freight) DESC LIMIT 1"},
    {"q": "Which city has the highest total onHand stock in end_inventory? Return City and the total.",
     "gold_sql": "SELECT City, SUM(onHand) FROM end_inventory GROUP BY City ORDER BY SUM(onHand) DESC LIMIT 1"},

    # --- multi-step (tests calculation / subquery) ---
    {"q": "What is the ratio of total purchase Dollars in the purchases table to total SalesDollars in the sales table, rounded to 2 decimals? Return a single number.",
     "gold_sql": "SELECT ROUND((SELECT SUM(Dollars) FROM purchases) * 1.0 / (SELECT SUM(SalesDollars) FROM sales), 2)"},
    {"q": "How many distinct brands did we purchase from the vendor with the highest total purchase Dollars? Return a single number.",
     "gold_sql": ("SELECT COUNT(DISTINCT Brand) FROM purchases WHERE VendorName = "
                  "(SELECT VendorName FROM purchases GROUP BY VendorName ORDER BY SUM(Dollars) DESC LIMIT 1)")},
]


def check_gold(db_path="inventory.db"):
    """Run every gold SQL and print the first rows so you can sanity-check by eye."""
    import sqlite3
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    for i, c in enumerate(GOLDEN, 1):
        rows = conn.execute(c["gold_sql"]).fetchall()
        print(f"{i:>2}. {c['q']}\n    -> {rows[:5]}\n")


if __name__ == "__main__":
    check_gold()
