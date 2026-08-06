# 📊 End-to-End Vendor Sales Analytics & Business Intelligence Dashboard

![Dashboard Preview](https://github.com/user-attachments/assets/6bd1ba17-8748-4379-accb-afcfd9a0e578)

An end-to-end data analytics project that transforms raw vendor transaction data into actionable business insights using **SQL, Python (Pandas, NumPy, SciPy), Exploratory Data Analysis, Statistical Hypothesis Testing, and Power BI**.

The project demonstrates a complete analytics workflow: data ingestion → SQL querying → feature engineering → statistical analysis → visualization → dashboard development.

---

## 🎯 Business Problem

Organizations dealing with thousands of purchase and sales transactions across multiple vendors and brands often struggle to answer key questions such as:

- Which vendors generate the highest revenue?
- Which vendors are the most profitable?
- Which brands contribute the most to total sales?
- Does purchasing in bulk actually reduce unit price — and is that effect statistically real?
- How much does freight cost affect profitability, and is it distributed evenly across vendors?
- Which vendors should the business prioritize?

This project answers these questions by combining SQL, Python, statistical testing, and Power BI into one analytics pipeline.

---

## 📂 Dataset

| Detail | Value |
|---|---|
| Original dataset size | ~2 GB |
| Total records (full dataset, estimated) | ~1.6–1.8 crore (~16–18 million) |
| Confirmed source rows (excl. `sales.csv`, ~2GB) | ~28.2 lakh (2,821,296 across begin/end inventory, purchases, vendor invoice, purchase prices) |
| Database | SQLite |

Combines multiple source tables:
- Sales
- Purchases (2,372,475 line items)
- Purchase Prices
- Vendor Invoice (5,543 invoices)
- Beginning Inventory
- Ending Inventory

> **Note:** Due to GitHub's file size limits, the full dataset isn't included in this repository. A representative sample is provided in `/data`, and all scripts needed to reproduce the full analysis are included.

> ⚠️ If your dashboard KPIs (below) reflect a sample rather than the full 2GB/20M-record dataset, say so explicitly — mismatched scale is the first thing an interviewer will ask about.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Data processing |
| Pandas | Data cleaning & manipulation |
| NumPy | Numerical operations |
| SciPy (`stats`) | Hypothesis testing, correlation, confidence intervals |
| SQLite | Database |
| SQL | Business queries |
| Matplotlib | Data visualization |
| Seaborn | Statistical visualization |
| Power BI | Dashboard development |

---

## 🔄 Project Workflow

```
Raw CSV Files
      ↓
SQLite Database
      ↓
SQL Aggregation & Joins
      ↓
Python Data Cleaning
      ↓
Feature Engineering
      ↓
Exploratory Data Analysis
      ↓
Statistical Hypothesis Testing
      ↓
Interactive Power BI Dashboard
      ↓
Business Insights
```

---

## 📁 Repository Structure

```
End-to-End-Vendor-Sales-Analytics
│
├── dashboard/
│   ├── project.py
│   └── vendorsalesanalysisdashboard.pbix
│
├── data/
│   └── sample CSV files
│
├── eda_and_logs/
│   ├── exploratorydata.py
│   ├── ingestion_db.py
│   ├── vendorperformanceanalysis.py
│   ├── statistical_analysis.py
│   └── ingestion.dblog
│
├── images/                  # charts referenced in this README
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🗄️ Database & SQL Analysis

Raw CSV files are imported into a SQLite database using chunk-based ingestion to efficiently handle large volumes of data.

**SQL techniques used:**
- Common Table Expressions (CTEs)
- LEFT JOIN
- GROUP BY + aggregate functions
- COALESCE()
- Business metric calculations

**Business metrics generated:**
- Total Sales
- Total Purchase Quantity
- Gross Profit
- Profit Margin
- Freight Cost
- Stock Turnover
- Sales-to-Purchase Ratio

![SQL Analysis](https://github.com/user-attachments/assets/351855c6-1052-4fd3-b0c7-d360336efb48)

---

## 🐍 Python: Data Cleaning & Feature Engineering

Python was used for data cleaning, missing-value handling, feature engineering, business metric calculation, statistical analysis, and aggregation.

![Feature Engineering](https://github.com/user-attachments/assets/eb9340e0-f914-4035-b20b-c88a464c991c)

**New features created:**
- Gross Profit
- Profit Margin
- Stock Turnover
- Sales-to-Purchase Ratio
- Order Size Categories
- Average Unit Price

![Engineered Features](https://github.com/user-attachments/assets/9fe58e04-05cd-461d-a29e-85c6085890b3)

---

## 📈 Exploratory Data Analysis

EDA was performed using Matplotlib and Seaborn to identify distributions, correlations, trends, and outliers before dashboard development.

![EDA Overview 1](https://github.com/user-attachments/assets/3c4b0125-487d-4b8e-bc80-06a7ae27a04b)
![EDA Overview 2](https://github.com/user-attachments/assets/d458d5b1-b7e7-4276-a6ed-fbd3809392a4)

### Distribution Analysis

![Distribution Analysis](https://github.com/user-attachments/assets/cf510d1c-fde6-428f-822f-2d7721b02077)

**Observations:**
- Most business variables show a right-skewed distribution.
- A small number of vendors contribute disproportionately high sales.
- Gross Profit varies significantly across vendors.
- Freight Cost has a few high-value outliers.

### Correlation Heatmap

![Correlation Heatmap](https://github.com/user-attachments/assets/9bbb5ce7-2ac7-44a2-9dcf-8b425b42155a)

**Key findings:**
- Total Sales and Total Purchase Dollars show strong positive correlation.
- Gross Profit correlates strongly with Sales.
- Profit Margin shows a *negative* correlation with Total Sales — high-volume vendors tend to run thinner margins.
- Stock Turnover has a moderate correlation with Profit Margin.

---

## 📐 Statistical Analysis & Hypothesis Testing

Beyond descriptive EDA, formal statistical tests (via `scipy.stats`) were run on the raw `purchases.csv` (2,372,321 valid line items) and `vendor_invoice.csv` (5,543 invoices) to validate business assumptions rather than just eyeball charts.

### 1. Does bulk purchasing reduce unit price?

| Order size bucket | Mean Purchase Price | Median | Count |
|---|---|---|---|
| Small (1–6 units) | $15.16 | $10.96 | 969,085 |
| Medium (7–12 units) | $10.01 | $7.99 | 1,024,143 |
| Large (13–24 units) | $10.78 | $8.14 | 188,576 |
| Bulk (25+ units) | $8.44 | $6.46 | 190,517 |

- **Pearson r** (Quantity vs. Price) = -0.083 — weak *linear* relationship
- **Spearman ρ** = -0.257 — a stronger *monotonic* (non-linear) relationship, meaning the effect exists but isn't a straight line
- **One-way ANOVA** across buckets: F = 17,351.09, **p < 0.001**

**Conclusion:** Bulk buying does reduce per-unit price, and the effect is statistically significant — but the relationship is non-linear, so a simple correlation coefficient understates it.

### 2. Freight cost outliers (IQR method)

- IQR bounds: **[-$331.94, $566.62]**
- **738 of 5,543 invoices (13.3%)** are freight outliers
- Mean freight per invoice: **$295.95**, 95% CI: **[$277.16, $314.74]**

### 3. Does freight scale efficiently with order size?

- **Pearson r** (Quantity vs. Freight) = **0.947**, p < 0.001

Freight cost scales almost linearly with order quantity — meaning freight isn't disproportionately punishing small vendors, it's simply proportional to volume shipped.

### 4. Are top vendors more freight-efficient? (Two-sample t-test)

| Group | Mean Freight/Unit | n |
|---|---|---|
| Top 10 vendors by $ volume | $0.06 | 550 |
| All other vendors | $0.07 | 4,993 |

- **Welch's t-test:** t = -7.07, **p = 2.5 × 10⁻¹²**

**Conclusion:** The difference is statistically significant — top vendors negotiate meaningfully better freight rates per unit, likely due to shipping scale/negotiating power.

---

## 📊 Power BI Dashboard

![Dashboard](https://github.com/user-attachments/assets/96ea49fa-af6a-470c-bc30-1c1f0e55e4ea)

**Dashboard features:**
- KPI cards — Total Sales, Gross Profit, Purchase Quantity, Freight Cost
- Vendor performance analysis
- Top 5 brand analysis
- Gross profit analysis
- Freight cost analysis
- Order size analysis
- Average unit price analysis
- Sales vs. freight cost scatter plot

---

## 💡 Key Business Insights

- A small set of top-performing vendors contributes the majority of total revenue — the **top 20% of vendors account for ~88% of total sales**, an even sharper concentration than the classic 80/20 rule.
- Bulk purchasing significantly reduces purchase price per unit (ANOVA p < 0.001), though the relationship is non-linear.
- Freight cost scales almost linearly with order quantity (r = 0.947) — it is not a disproportionate burden on smaller orders.
- Top-10 vendors are statistically more freight-efficient than the rest (p < 0.001), suggesting negotiating leverage from volume.
- Gross profit varies considerably by brand, with a small number of brands driving most profit.
- Medium-sized orders show the highest average unit price relative to large/bulk orders.

---

## 📊 Dashboard KPIs

| Metric | Value |
|---------|--------|
| Total Sales | $450.88M |
| Total Purchase Quantity | 33.58M units |
| Gross Profit | $128.98M |
| Profit Margin | 28.61% |
| Freight Cost | $1.64M |

*(Across 131 vendors, ~2 crore total source records once all six tables — sales, purchases, purchase prices, vendor invoice, beginning/ending inventory — are combined.)*

---

## 🚀 Skills Demonstrated

SQL · SQLite · Python · Pandas · NumPy · SciPy · Statistical Hypothesis Testing (t-test, ANOVA) · Correlation Analysis (Pearson & Spearman) · Confidence Intervals · Outlier Detection (IQR) · Data Cleaning · Data Wrangling · Feature Engineering · Exploratory Data Analysis · Matplotlib · Seaborn · Business Intelligence · Power BI · Dashboard Design · Business Analytics

---

## 🧩 Data Quality Challenge & Fix

While validating the aggregated metrics, a join issue was found: vendor-level fields (**Total Purchase Dollars**, **Total Purchase Quantity**, **Total Freight Cost**) were being repeated across *every brand row* belonging to that vendor — a classic one-to-many fan-out (e.g., a vendor carrying 449 brands had its purchase-dollar figure duplicated 449 times). A naive `SUM()` across brand-level rows therefore overstated these totals by orders of magnitude.

**Evidence of the bug:** the unfixed aggregation produced an average Gross Profit of **–$11.9 million per brand row** (clearly impossible) across 12,255 rows — a direct symptom of the fan-out duplicating large vendor-level totals thousands of times over.

**Fix:** deduplicated vendor-level fields at the vendor grain (one row per vendor) before summing, while brand-level fields (Sales, Gross Profit, Excise Tax) were summed directly since they are genuinely distinct per brand. This corrected the KPIs shown above.

---

## 📌 Future Improvements

- Interactive slicers and drill-through pages
- Power BI Service deployment
- Automated ETL pipeline
- SQL Server integration
- Predictive analytics (ML-based demand/profit forecasting)
- Incremental data refresh
- Extend hypothesis testing to vendor-level profit margin comparisons (ANOVA across vendor tiers)

---

## ▶️ How to Run

**1. Clone the repository**
```bash
git clone https://github.com/SambhavYatendraBhardwaj/End-to-End-Vendor-Sales-Analytics-Business-Intelligence-Dashboard.git
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run database ingestion**
```bash
python eda_and_logs/ingestion_db.py
```

**4. Run SQL aggregation & feature engineering**
```bash
python eda_and_logs/exploratorydata.py
```

**5. Run vendor performance analysis**
```bash
python eda_and_logs/vendorperformanceanalysis.py
```

**6. Run statistical analysis (hypothesis tests, correlations, CIs)**
```bash
python eda_and_logs/statistical_analysis.py
```

**7. Open the Power BI dashboard**
```
dashboard/vendorsalesanalysisdashboard.pbix
```

---

## 📌 Conclusion

This project demonstrates a complete end-to-end data analytics workflow — from ingesting large-scale transactional data into a database to generating statistically validated business insights through SQL, Python, EDA, hypothesis testing, and Power BI. It reflects practical skills in data cleaning, SQL querying, feature engineering, statistical inference, dashboard development, and business intelligence reporting, relevant to Data Analyst and BI roles.

---

## 👨‍💻 Author

**Sambhav Yatendra Bhardwaj**
Aspiring Data Analyst

📧 sambhavbhardwaj029@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/sambhav-yatendra-bhardwaj-021403303)
🐙 [GitHub](https://github.com/SambhavYatendraBhardwaj)

## 📝 License

This project is open-source and available under the MIT License.
