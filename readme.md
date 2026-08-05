<img width="1917" height="1025" alt="Screenshot 2026-08-05 121848" src="https://github.com/user-attachments/assets/f73df62b-4585-4a5c-bb12-8ad17060a6b1" /># 📊 End-to-End Vendor Sales Analytics & Business Intelligence Dashboard
<img width="1168" height="663" alt="Screenshot 2026-08-05 121701" src="https://github.com/user-attachments/assets/6bd1ba17-8748-4379-accb-afcfd9a0e578" />
An end-to-end Data Analytics project that transforms raw vendor transaction data into actionable business insights using **SQL, Python, Pandas, Exploratory Data Analysis (EDA), and Power BI**.

The project demonstrates a complete analytics workflow including **data ingestion, SQL querying, feature engineering, statistical analysis, visualization, and dashboard development**.

---

# 🎯 Business Problem

Organizations often deal with thousands of purchase and sales transactions across multiple vendors and brands. Without proper analysis, it becomes difficult to answer important business questions such as:

- Which vendors generate the highest revenue?
- Which vendors are the most profitable?
- Which brands contribute the most to total sales?
- Does purchasing in bulk reduce purchase price?
- How much freight cost affects profitability?
- Which vendors should the business prioritize?

This project answers these questions by combining SQL, Python, and Power BI into one complete analytics pipeline.

---

# 📂 Dataset

**Original Dataset Size:** ~2 GB

**Total Records:** Approximately 2+ Crore

**Database:** SQLite

The project combines multiple datasets including:

- Sales
- Purchases
- Purchase Prices
- Vendor Invoice
- Beginning Inventory
- Ending Inventory

> **Note:** Due to GitHub's file size limitations, the original dataset is not included in this repository. All scripts required to reproduce the complete analysis are available.

---

# 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data Processing |
| Pandas | Data Cleaning & Manipulation |
| NumPy | Numerical Operations |
| SQLite | Database |
| SQL | Business Queries |
| Matplotlib | Data Visualization |
| Seaborn | Statistical Visualization |
| Power BI | Dashboard Development |

---

# 🔄 Project Workflow

```text
Raw CSV Files
        │
        ▼
SQLite Database
        │
        ▼
SQL Aggregation & Joins
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
Interactive Power BI Dashboard
        │
        ▼
Business Insights
```

---

# 📁 Repository Structure

```text
End-to-End-Vendor-Sales-Analytics

│
├── dashboard
│   ├── project.py
│   └── vendorsalesanalysisdashboard.pbix
│
├── data
│   ├── Sample CSV Files
│
├── eda_and_logs
│   ├── exploratorydata.py
│   ├── ingestion_db.py
│   ├── vendorperformanceanalysis.py
│   └── ingestion.dblog
│
├── README.md
└── .gitignore
```

---

# 🗄️ Database & SQL Analysis

The raw CSV files are imported into a SQLite database using chunk-based ingestion to efficiently handle large datasets.

SQL operations performed include:

- Common Table Expressions (CTEs)
- LEFT JOIN
- GROUP BY
- Aggregate Functions
- COALESCE()
- Business Metric Calculations

Business metrics generated:

- Total Sales
- Total Purchase Quantity
- Gross Profit
- Profit Margin
- Freight Cost
- Stock Turnover
- Sales Purchase Ratio
- <img width="1897" height="1007" alt="Screenshot 2026-08-05 121937" src="https://github.com/user-attachments/assets/351855c6-1052-4fd3-b0c7-d360336efb48" />


---

# 🐍 Python Data Cleaning & Feature Engineering

Python was used for:

- Data Cleaning
- Missing Value Handling
- Feature Engineering
- Business Metric Calculation
- Statistical Analysis
- Data Aggregation
<img width="1116" height="662" alt="Screenshot 2026-08-05 123021" src="https://github.com/user-attachments/assets/eb9340e0-f914-4035-b20b-c88a464c991c" />

New features created:

- Gross Profit
- Profit Margin
- Stock Turnover
- Sales Purchase Ratio
- Order Size Categories
- Average Unit Price
- <img width="1107" height="820" alt="Screenshot 2026-08-05 121930" src="https://github.com/user-attachments/assets/9fe58e04-05cd-461d-a29e-85c6085890b3" />


---

# 📈 Exploratory Data Analysis

EDA was performed using **Matplotlib** and **Seaborn** to identify distributions, correlations, trends, and outliers before dashboard development.
<img width="1917" height="1017" alt="Screenshot 2026-08-05 122905" src="https://github.com/user-attachments/assets/3c4b0125-487d-4b8e-bc80-06a7ae27a04b" />
<img width="1917" height="1026" alt="Screenshot 2026-08-05 122854" src="https://github.com/user-attachments/assets/d458d5b1-b7e7-4276-a6ed-fbd3809392a4" />
---

## 📊 Distribution Analysis

<img src="images/distribution_analysis.png" width="900">

<img width="1917" height="1017" alt="Screenshot 2026-08-05 122905" src="https://github.com/user-attachments/assets/cf510d1c-fde6-428f-822f-2d7721b02077" />


### Observations

- Most business variables exhibit a right-skewed distribution.
- A small number of vendors contribute disproportionately high sales.
- Gross Profit varies significantly across vendors.
- Freight Cost contains a few high-value observations.

---

## 🔥 Correlation Heatmap

<img width="1917" height="1023" alt="Screenshot 2026-08-05 123327" src="https://github.com/user-attachments/assets/9bbb5ce7-2ac7-44a2-9dcf-8b425b42155a" />



### Key Findings

- Total Sales Dollars and Total Purchase Dollars show strong positive correlation.
- Gross Profit has a strong positive relationship with Sales.
- Profit Margin shows a negative correlation with Total Sales.
- Stock Turnover has moderate correlation with Profit Margin.

---

# 📊 Power BI Dashboard

The final dashboard provides an interactive overview of vendor performance.

## Dashboard Preview


<img width="1917" height="1017" alt="Screenshot 2026-08-05 122905" src="https://github.com/user-attachments/assets/2ac6ed45-3bfa-47a1-afde-4f758dcd85e2" />
<img width="1917" height="1017" alt="Screenshot 2026-08-05 122905" src="https://github.com/user-attachments/assets/65d0198d-079b-42c4-b139-0222b7e7b955" />
<img width="1186" height="703" alt="Screenshot 2026-08-05 123407" src="https://github.com/user-attachments/assets/96ea49fa-af6a-470c-bc30-1c1f0e55e4ea" />


---

## Dashboard Features

✔ KPI Cards

- Total Sales
- Gross Profit
- Purchase Quantity
- Freight Cost

✔ Vendor Performance Analysis

✔ Top 5 Brand Analysis

✔ Gross Profit Analysis

✔ Freight Cost Analysis

✔ Order Size Analysis

✔ Average Unit Price Analysis

✔ Sales vs Freight Cost Scatter Plot

---

# 💡 Key Business Insights

- Top-performing vendors contribute the majority of total revenue.
- Bulk purchasing generally reduces purchase price.
- Freight cost differs significantly across vendors.
- Medium-sized orders generate the highest average unit price.
- Gross Profit varies considerably among brands.
- A small number of brands account for most of the overall sales, following the Pareto Principle (80/20 Rule).

---

# 📊 Dashboard KPIs

| Metric | Value |
|---------|--------|
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
- Exploratory Data Analysis
- Business Intelligence
- Power BI
- Dashboard Design
- Data Visualization
- Business Analytics

---

# 📌 Future Improvements

- Interactive slicers
- Drill-through pages
- Power BI Service Deployment
- Automated ETL Pipeline
- SQL Server Integration
- Predictive Analytics using Machine Learning
- Incremental Data Refresh

---

# ▶️ How to Run

Clone the repository

```bash
git clone https://github.com/SambhavYatendraBhardwaj/End-to-End-Vendor-Sales-Analytics-Business-Intelligence-Dashboard.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run database ingestion

```bash
python ingestion_db.py
```

Run SQL aggregation & feature engineering

```bash
python exploratorydata.py
```

Run vendor performance analysis

```bash
python vendorperformanceanalysis.py
```

Open the Power BI dashboard

```text
vendorsalesanalysisdashboard.pbix
```

---

# 📌 Conclusion

This project demonstrates a complete end-to-end data analytics workflow, from ingesting large-scale transactional data into a database to generating business insights through SQL, Python, exploratory data analysis, and Power BI.

It showcases practical skills in **data cleaning, SQL querying, feature engineering, statistical analysis, dashboard development, and business intelligence reporting**, making it suitable for real-world Data Analyst and Business Intelligence roles.

---

# 👨‍💻 Author

**Sambhav Yatendra Bhardwaj**

GitHub: https://github.com/SambhavYatendraBhardwaj
