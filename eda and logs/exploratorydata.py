import pandas as pd
import sqlite3
from IPython.display import display

conn = sqlite3.connect("inventory.db")
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'", conn
)

for table in tables["name"]:
    print(f"\n======== Previewing Table: {table} ========")

    # 1. Row count print karo
    count = pd.read_sql(f"SELECT COUNT(*) AS count FROM {table}", conn)[
        "count"
    ].values[0]
    print(f"Total Records: {count:,}")

    # 2. Pehley 5 rows ka visual display karo
    df_preview = pd.read_sql(f"SELECT * FROM {table} LIMIT 5", conn)
    display(df_preview)
pur=pd.read_sql_query("select * from purchases WHERE VendorNumber=4466",conn)
print(pur)
purchase_prices=pd.read_sql_query("select * from purchase_prices WHERE VendorNumber=4466",conn)
print(purchase_prices)
# print(purchases.groupby(["Brand","PurchasePrice"])[["Quantity","Dollars"]].sum())
# print(vendor_invoice)
vendor_invoice = pd.read_csv("data/vendor_invoice.csv")
print(vendor_invoice)
print((vendor_invoice["PONumber"]).nunique())
print(vendor_invoice.columns)
# sales=pd.read_csv("data/sales.csv")
# print(sales)
# print(sales.groupby('Brand')[["SalesQuantity","SalesPrice"]].sum())
# print(pd.read_csv("data/vendor_invoice.csv"))
# print(pd.read_sql_query("select VendorName,SUM(Freight) as freight FROM vendor_invoice GROUP BY VendorName",conn))
# sales=pd.read_csv("data/sales.csv")
# print(sales.columns)
# print(pd.read_sql_query("select VendorNo,VendorName,Brand,SUM(SalesDollars) as totalsalesdollars,SUM(SalesPrice) as totalsalesprice,SUM(SalesQuantity) as totalsalesquantity FROM sales GROUP BY VendorNo,Brand",conn))
import time
import pandas as pd

start = time.time()

query = """
WITH sales_summary AS (
    SELECT 
        VendorNo,
        Brand,
        SUM(SalesQuantity) AS TotalSalesQuantity,
        SUM(SalesDollars) AS TotalSalesDollars,
        SUM(SalesPrice) AS TotalSalesPrice,
        SUM(ExciseTax) AS TotalExciseTax
    FROM sales
    GROUP BY VendorNo, Brand
),
invoice_summary AS (
    SELECT 
        VendorNumber,
        SUM(Quantity) AS TotalPurchaseQuantity,
        SUM(Dollars) AS TotalPurchaseDollars,
        SUM(Freight) AS TotalFreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
)
SELECT 
    pp.VendorNumber,
    pp.Brand,
    pp.Price AS ActualPrice,
    pp.PurchasePrice,
    COALESCE(s.TotalSalesQuantity, 0) AS TotalSalesQuantity,
    COALESCE(s.TotalSalesDollars, 0) AS TotalSalesDollars,
    COALESCE(s.TotalSalesPrice, 0) AS TotalSalesPrice,
    COALESCE(s.TotalExciseTax, 0) AS TotalExciseTax,
    COALESCE(vi.TotalPurchaseQuantity, 0) AS TotalPurchaseQuantity,
    COALESCE(vi.TotalPurchaseDollars, 0) AS TotalPurchaseDollars,
    COALESCE(vi.TotalFreightCost, 0) AS TotalFreightCost
FROM purchase_prices pp
LEFT JOIN sales_summary s 
    ON pp.VendorNumber = s.VendorNo 
    AND pp.Brand = s.Brand
LEFT JOIN invoice_summary vi 
    ON pp.VendorNumber = vi.VendorNumber;
"""

final_table = pd.read_sql_query(query, conn)

end = time.time()
print(f"Time taken: {end - start:.2f} seconds")
print(final_table)
# print(final_table.dtypes)
# print(final_table.isnull().sum())
print(final_table.columns)
final_table['GrossProfit']=final_table['TotalSalesDollars']-final_table['TotalPurchaseDollars']
# print(final_table.columns)
final_table['Profitmargin']=final_table['GrossProfit']/final_table['TotalSalesDollars']
final_table['StockTurnover']=final_table["TotalSalesDollars"]/final_table["TotalPurchaseQuantity"]
final_table["SalesPurchaseRatio"]=final_table["TotalSalesDollars"]/final_table["TotalPurchaseDollars"]
print(final_table.columns)
# 'data' folder ke andar save karne ke liye
final_table.to_csv("data/final_summary.csv", index=False)
print("file successfully saved")
conn.close()

