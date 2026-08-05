import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import warnings
import sqlite3
from scipy.stats import ttest_ind
import scipy.stats as stats

warnings.filterwarnings('ignore')

conn = sqlite3.connect('inventory.db')

# 1. Pehle CSV read karein
df = pd.read_csv("data/final_summary.csv")

# 2. Isse database me 'final_summary' table banakar save karein
df.to_sql("final_summary", conn, if_exists="replace", index=False)

# 3. Ab SQL query chalayein
df = pd.read_sql_query("SELECT * FROM final_summary", conn)
print(df.head())
print(df.describe().T)
# numerical_cols=df.select_dtypes(include=np.number).columns
# plt.figure(figsize=(15,10))
# for i ,col in enumerate (numerical_cols):
#     plt.subplot(4,4,i+1)
#     sns.histplot(df[col],kde=True,bins=30)
#     plt.title(col)
# plt.tight_layout()
# plt.show()
# numerical_cols=df.select_dtypes(include=np.number).columns
# plt.figure(figsize=(15,10))
# for i ,col in enumerate (numerical_cols):
#     plt.subplot(4,4,i+1)
#     sns.boxplot(y=df[col])
#     plt.title(col)
# plt.tight_layout()
# plt.show()
df=pd.read_sql_query("select * from final_summary WHERE GrossProfit>0 AND ProfitMargin>0 AND TotalSalesQuantity>0",conn)
print(df)
# numerical_cols=df.select_dtypes(include=np.number).columns
# plt.figure(figsize=(15,10))
# for i ,col in enumerate (numerical_cols):
#     plt.subplot(4,4,i+1)
#     sns.histplot(df[col],kde=True,bins=30)
#     plt.title(col)
# plt.tight_layout()
# plt.show()
# categorical_cols=["Brand","GrossProfit"]
# plt.figure(figsize=(12,5))
# for i,col in enumerate(categorical_cols):
#     plt.subplot(1,2,i+1)
#     sns.countplot(y=df[col],order=df[col].value_counts().index[:10])
#     plt.title(f"count plot of {col}")
# plt.tight_layout()
# plt.show()
# plt.figure(figsize=(12,8))
# correlation_matrix=df[numerical_cols].corr()
# sns.heatmap(correlation_matrix,annot=True,fmt=".2f",cmap="coolwarm",linewidth=0.5)
# plt.title("correlation heatmap")
# plt.show()
# brand_performance=df.groupby("Brand").agg({
#     'TotalSalesDollars':'sum',
#     'Profitmargin':'mean',
# }).reset_index()
# print(brand_performance)
# highest_sales=df.groupby("VendorNumber")["TotalSalesDollars"].sum().nlargest(10)
# print(highest_sales)
# group=df.groupby('VendorNumber').agg({
#     "TotalPurchaseDollars":"sum",
#     "GrossProfit":"sum",
#     "TotalSalesDollars":"sum"
# })
# print(group)
# Total Sales me har row ka % share calculate karne ke liye:
df["sales_percentage"] = (
    df["TotalSalesPrice"] / df["TotalSalesPrice"].sum()
) * 100

print(df)
# import matplotlib.pyplot as plt
# import seaborn as sns

# # 1. Canvas aur main axis setup
# fig, ax1 = plt.subplots(figsize=(10, 6))

# # 2. Purchase Contribution% ke liye Bar Plot (ax1 par)
# sns.barplot(
#     x=df['VendorNumber'], 
#     y=df['sales_percentage'], 
#     palette='mako', 
#     ax=ax1
# )

# # Har bar ke andar exact percentage label place karne ke liye
# for i, value in enumerate(df['sales_percentage']):
#     ax1.text(
#         i, 
#         value - 1, 
#         f"{str(round(value, 1))}%", 
#         ha='center', 
#         fontsize=10, 
#         color='white'
#     )

# # 3. Dual Axis create karna Cumulative % Line ke liye
# ax2 = ax1.twinx()

# # Cumulative Contribution% ke liye Red Line Plot (ax2 par)
# ax2.plot(
#     df['VendorNumber'], 
#     df['TotalSalesPrice'], 
#     color='red', 
#     marker='o', 
#     linestyle='dashed', 
#     label='Cumulative Contribution%'
# )

# # 4. Labels, Titles aur Rotations format karna
# ax1.set_xticklabels(df['VendorNumber'], rotation=90)
# ax1.set_ylabel('sales_percentage', color='blue')
# ax2.set_ylabel('TotalSalesPrice', color='red')
# ax1.set_xlabel('Vendors')
# ax1.set_title('Pareto Chart: Vendor Contribution to Total Purchases')

# # 5. Reference 100% line aur Legend set karna
# ax2.axhline(y=100, color='gray', linestyle='dashed', alpha=0.7)
# ax2.legend(loc='upper right')

# plt.tight_layout()
# plt.show()

# Does purchasing in bulk readuces the unit price

df["unitprice"]=df["TotalSalesPrice"]/df["TotalSalesQuantity"]
print(df)
df["order_size"]=pd.qcut(df["TotalPurchaseQuantity"],q=3,labels=['small','medium','large'])
print(df)
print(df.groupby('order_size')["unitprice"].mean())
df.to_csv("data/final.csv", index=False)
print("file successfully saved")