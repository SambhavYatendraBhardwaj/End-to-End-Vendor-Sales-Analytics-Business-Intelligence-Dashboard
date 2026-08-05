# 📊 End-to-End Vendor Sales Analytics & Business Intelligence Dashboard

An end-to-end Data Analytics project that analyzes vendor sales performance, procurement efficiency, freight costs, and profitability using SQL, Python, Pandas, Exploratory Data Analysis (EDA), and Power BI.

This project demonstrates the complete analytics workflow from raw data ingestion to business intelligence reporting.

---

# 📌 Business Problem

Businesses often struggle to identify:

- Which vendors generate the highest revenue?
- Which vendors are the most profitable?
- Does purchasing in bulk reduce unit price?
- Which brands contribute the most to sales?
- How much freight cost affects profitability?

This project answers these business questions by combining SQL, Python, and Power BI into one complete analytics pipeline.

---

# 📂 Dataset

- Original Dataset Size: **~2 GB**
- Total Records: **Approximately 2+ Crore Records**
- Database: **SQLite**
- Multiple CSV files integrated into a relational database.

> **Note:** The original dataset is not included because it exceeds GitHub's file size limit. All scripts required to reproduce the analysis are available in this repository.

---

# 🛠️ Tech Stack

| Tool | Purpose |
|------|----------|
| Python | Data Processing |
| Pandas | Data Cleaning & Manipulation |
| NumPy | Numerical Operations |
| SQLite | SQL Database |
| SQL | Business Queries |
| Matplotlib | Data Visualization |
| Seaborn | Statistical Visualization |
| Power BI | Interactive Dashboard |

---

# 🔄 Project Workflow

```
Raw CSV Files
        │
        ▼
SQLite Database
        │
        ▼
SQL Queries & Joins
        │
        ▼
Python Data Cleaning
        │
        ▼
Feature Engineering
        │
        ▼
Exploratory Data Analysis
        │
        ▼
Power BI Dashboard
        │
        ▼
Business Insights
```

---

# 📁 Repository Structure

```
End-to-End-Vendor-Sales-Analytics/

│
├── dashboard/
│   ├── project.py
│   └── VendorSalesAnalysisDashboard.pbix
│
├── eda and logs/
│   ├── ingestion_db.py
│   ├── exploratorydata.py
│   ├── vendorperformanceanalysis.py
│   └── ingestion.dblog
│
├── README.md
├── .gitignore
```

---

# 🗄️ Database & SQL Analysis

The project begins by loading multiple CSV files into a SQLite database using chunk-based ingestion for handling large datasets efficiently.

SQL operations performed include:

- Common Table Expressions (CTEs)
- LEFT JOIN
- GROUP BY
- Aggregate Functions
- COALESCE()
- Business Metric Calculations

Generated metrics include:

- Total Sales
- Purchase Quantity
- Gross Profit
- Profit Margin
- Freight Cost
- Sales Purchase Ratio
- Stock Turnover

---

# 🐍 Python Analysis

Python was used for:

- Data Cleaning
- Missing Value Handling
- Feature Engineering
- Business Metric Calculation
- Statistical Analysis
- Data Aggregation

Additional features created:

- Gross Profit
- Profit Margin
- Sales Percentage
- Unit Price
- Order Size Categories
- Sales Purchase Ratio
- Stock Turnover

---

# 📈 Exploratory Data Analysis (EDA)

EDA was performed using Matplotlib and Seaborn.

Visualizations include:

- Distribution Plots
- Box Plots
- Correlation Heatmaps
- Brand Analysis
- Vendor Performance Analysis
- Purchase Behaviour Analysis
- Sales Distribution

---

# 📊 Power BI Dashboard

Dashboard includes:

- Total Sales KPI
- Total Purchase Quantity
- Gross Profit KPI
- Freight Cost KPI
- Top 5 Brands
- Gross Profit by Brand
- Vendor Sales vs Freight Cost
- Order Size Analysis
- Average Unit Price Analysis

---

# 📷 Dashboard Preview

![Vendor Dashboard](dashboard_preview.png)

---

# 💡 Key Business Insights

- Top-performing vendors contribute a major share of total revenue.
- Bulk purchasing generally reduces unit price.
- Freight cost varies significantly across vendors.
- Medium-sized orders have the highest average unit price.
- Gross profit differs substantially across brands.
- A small number of brands generate the majority of sales (Pareto Principle).

---

# 📌 Dashboard KPIs

| Metric | Value |
|---------|-------|
| Total Sales | $333.01K |
| Purchase Quantity | 23K |
| Gross Profit | $46.30K |
| Freight Cost | $1.47K |

---

# 🚀 Skills Demonstrated

- SQL
- SQLite
- Python
- Pandas
- NumPy
- Data Cleaning
- Data Wrangling
- Feature Engineering
- Exploratory Data Analysis (EDA)
- Business Intelligence
- Power BI
- Data Visualization
- Business Analytics
- Dashboard Design

---

# 🔮 Future Improvements

- Interactive slicers
- Drill-through reports
- Power BI Service deployment
- Automated ETL pipeline
- Incremental Data Refresh
- SQL Server integration
- Predictive Analytics using Machine Learning

---

# ▶️ How to Run

1. Clone the repository

```
git clone https://github.com/yourusername/End-to-End-Vendor-Sales-Analytics.git
```

2. Install dependencies

```
pip install -r requirements.txt
```

3. Run data ingestion

```
python ingestion_db.py
```

4. Run SQL & feature engineering

```
python exploratorydata.py
```

5. Run analysis

```
python vendorperformanceanalysis.py
```

6. Open the Power BI Dashboard (.pbix)

---

# 📌 Conclusion

This project demonstrates a complete end-to-end data analytics workflow by integrating SQL, Python, Exploratory Data Analysis, and Power BI to transform raw transactional data into meaningful business insights. It showcases practical skills in data cleaning, feature engineering, business analysis, dashboard development, and decision support reporting, making it suitable for real-world Data Analyst and Business Intelligence scenarios.
