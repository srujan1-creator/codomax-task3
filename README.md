# Codomax Internship — Module 3: Data Analysis & Visualization

[![Python Version](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests Passing](https://img.shields.io/badge/Tests-14%2F14%20Passed-brightgreen.svg)]()
[![Module](https://img.shields.io/badge/Codomax-Module%203%20(Day%209--12)-orange.svg)]()
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/)

> **Submission Deliverables for Module 3 (Day 9 – Day 12 · Intermediate · High Priority)**  
> **Topic:** Data Analysis & Visualization with NumPy, Pandas, and Matplotlib  
> **Google Colab Notebook:** [`codomax_module3_data_analysis.ipynb`](./codomax_module3_data_analysis.ipynb)  
> **Learning Journal:** Available in [`LEARNING_NOTES.md`](./LEARNING_NOTES.md) (comprehensive Day 9 to Day 12 engineering notes)

---

## 📌 Table of Contents
1. [Project Overview](#-project-overview)
2. [Curriculum Coverage (Day 9 – Day 12)](#-curriculum-coverage-day-9--day-12)
3. [Architecture & Project Structure](#-architecture--project-structure)
4. [Dataset Specifications](#-dataset-specifications)
5. [Key Analytical Findings & KPIs](#-key-analytical-findings--kpis)
6. [Data Visualizations Showcase](#-data-visualizations-showcase)
   - [1. Bar Charts](#1-bar-charts)
   - [2. Line Charts](#2-line-charts)
   - [3. Pie & Donut Charts](#3-pie--donut-charts)
   - [4. Advanced Scatter & Correlation Heatmap](#4-advanced-scatter--correlation-heatmap)
   - [5. Consolidated Executive Dashboard](#5-consolidated-executive-dashboard)
7. [Running Locally](#-running-locally)
8. [Automated Unit Testing (14/14 Passing)](#-automated-unit-testing)
9. [Step-by-Step Google Colab Submission Guide](#-step-by-step-google-colab-submission-guide)
10. [Submission Checklist](#-submission-checklist)

---

## 🚀 Project Overview

As part of **Module 3: Data Analysis & Visualization (Day 9 – Day 12)** of the **Codomax Internship Program**, this repository delivers an end-to-end data analytics and visual storytelling suite.

The project demonstrates:
- Vectorized array operations and mathematical analysis using **NumPy**.
- Tabular manipulation, filtering, aggregation, and pivot modeling using **Pandas**.
- Rigorous exploratory data analysis (EDA) and data cleaning (handling nulls, deduplication, string sanitization, and IQR outlier detection).
- Publication-grade chart generation using **Matplotlib** and **Seaborn**, featuring bar charts, line charts, pie charts, donut charts, scatter plots, and an executive multi-panel dashboard.
- A fully pre-rendered, self-contained **Google Colab Notebook (`codomax_module3_data_analysis.ipynb`)** ready for 1-click execution and portal submission.

---

## 📚 Curriculum Coverage (Day 9 – Day 12)

| Day | Focus Area | Implemented Capabilities |
| :--- | :--- | :--- |
| **Day 9** | **NumPy & Pandas Foundations** | 1D & 2D arrays, vectorization, universal functions (`mean`, `std`, `sum`), boolean masks, Series and DataFrame structures, `.loc` vs. `.iloc` indexing, vectorized arithmetic. |
| **Day 10** | **Dataset Loading & EDA** | Loading 1,200 transaction records, `.head()`, `.tail()`, `.shape`, `.info()`, `.describe()`, categorical cardinality checks, null audits. |
| **Day 11** | **Data Cleaning & Deep Analysis** | Deduplication, string stripping, median/mode missing value imputation, datetime feature extraction, IQR outlier detection, `groupby` aggregations, pivot tables, correlation matrix. |
| **Day 12** | **Matplotlib & Seaborn Visualizations** | Dual bar charts, horizontal rankings, time-series line trends, regional multi-line trajectory, exploded pie chart, donut chart, scatter plot, correlation heatmap, 2×2 Executive Dashboard. |

---

## 🏗️ Architecture & Project Structure

The project maintains clean modularity across data loading, cleaning, analysis, visualization, and automated testing:

```
codomax-task3/
├── codomax_module3_data_analysis.ipynb  # Primary Deliverable: Google Colab Ready Notebook
├── main.py                             # CLI runner for local end-to-end pipeline execution
├── build_notebook.py                   # Programmatic builder & pre-execution script
├── requirements.txt                    # Python environment dependencies
├── README.md                           # Comprehensive documentation & submission guide
├── LEARNING_NOTES.md                   # In-depth Day 9 to Day 12 learning journal
├── LICENSE                             # MIT Open Source License
├── data/                               # Dataset storage
│   ├── ecommerce_sales_dataset.csv     # Raw dataset with intentional real-world quirks
│   └── cleaned_sales_dataset.csv       # Preprocessed and validated dataset
├── src/                                # Core modular Python package
│   ├── __init__.py                     # Package entrypoint
│   ├── data_loader.py                  # Dataset generation and CSV loading
│   ├── data_cleaner.py                 # Imputation, deduplication, IQR outlier detection
│   ├── data_analyzer.py                # Vectorized KPIs, groupbys, pivot tables, correlations
│   └── data_visualizer.py              # Matplotlib & Seaborn chart rendering engine
├── charts/                             # Exported high-resolution chart images (.png)
│   ├── 01_bar_chart_sales_profit_by_category.png
│   ├── 02_bar_chart_top10_subcategories.png
│   ├── 03_line_chart_monthly_sales_trend.png
│   ├── 04_line_chart_regional_trends.png
│   ├── 05_pie_chart_customer_segments.png
│   ├── 06_donut_chart_payment_methods.png
│   ├── 07_scatter_discount_vs_profit.png
│   ├── 08_correlation_heatmap.png
│   └── 09_executive_dashboard.png
└── tests/                              # Automated unit tests (14/14 passing)
    ├── __init__.py
    ├── test_data_cleaning.py
    ├── test_data_analysis.py
    └── test_visualization.py
```

---

## 📊 Dataset Specifications

The dataset models a full calendar year (2023) of retail transactions:
- **Observations:** 1,200 unique records (plus 5 duplicate rows in raw data for cleaning testing).
- **Features:** 14 attributes spanning financial, operational, temporal, and customer dimensions:
  - `Order_ID`, `Order_Date`, `Customer_ID`, `Segment`, `Region`
  - `Category`, `Sub_Category`, `Unit_Price`, `Quantity`, `Discount`, `Sales`, `Profit`
  - `Payment_Method`, `Customer_Rating`
- **Data Hygiene Scenarios:**
  - Missing ratings (~3%), missing payment methods (~2%), missing discounts (~1.5%).
  - Padded whitespace in strings (`" Technology "`).
  - Duplicate transaction rows.

---

## 📈 Key Analytical Findings & KPIs

```
==================================================
           EXECUTIVE KPI SUMMARY
==================================================
  Total Revenue:           $1,029,295.61
  Total Profit:            $255,566.54
  Net Profit Margin:       24.83%
  Total Units Sold:        3,128
  Average Order Value:     $857.75
  Median Order Value:      $442.10
  Average Customer Rating: 3.69 / 5.0
==================================================
```

### Performance by Category:
| Category | Total Sales ($) | Total Profit ($) | Avg Order Value ($) | Units Sold | Profit Margin (%) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Technology** | $662,301.48 | $176,710.52 | $1,627.28 | 1,058 | **26.68%** |
| **Furniture** | $285,248.30 | $45,648.84 | $796.78 | 937 | **16.00%** |
| **Office Supplies** | $81,745.83 | $33,207.18 | $187.92 | 1,133 | **40.62%** |

---

## 🎨 Data Visualizations Showcase

All charts are generated using **Matplotlib** and **Seaborn** with professional color schemes, clean typography, grid lines, and direct value labels.

### 1. Bar Charts
- **Sales & Profit by Category:** Dual-column comparison with dollar annotations.
  - File: [`charts/01_bar_chart_sales_profit_by_category.png`](./charts/01_bar_chart_sales_profit_by_category.png)
- **Top 10 Sub-Categories by Sales:** Horizontal ranked bar chart.
  - File: [`charts/02_bar_chart_top10_subcategories.png`](./charts/02_bar_chart_top10_subcategories.png)

### 2. Line Charts
- **Monthly Sales & Profit Trend (2023):** Dual line trajectory with shaded area fill.
  - File: [`charts/03_line_chart_monthly_sales_trend.png`](./charts/03_line_chart_monthly_sales_trend.png)
- **Regional Trajectory Comparison:** Multi-line tracking across North, South, East, West, Central.
  - File: [`charts/04_line_chart_regional_trends.png`](./charts/04_line_chart_regional_trends.png)

### 3. Pie & Donut Charts
- **Customer Segment Share:** Exploded slice highlighting the lead Consumer segment (50.5%).
  - File: [`charts/05_pie_chart_customer_segments.png`](./charts/05_pie_chart_customer_segments.png)
- **Payment Method Distribution:** Clean Donut chart with inner white circle cutout.
  - File: [`charts/06_donut_chart_payment_methods.png`](./charts/06_donut_chart_payment_methods.png)

### 4. Advanced Scatter & Correlation Heatmap
- **Discount Rate vs. Profitability:** Scatter plot showing break-even threshold at $0 profit.
  - File: [`charts/07_scatter_discount_vs_profit.png`](./charts/07_scatter_discount_vs_profit.png)
- **Correlation Heatmap:** Seaborn annotated Pearson matrix of numeric variables.
  - File: [`charts/08_correlation_heatmap.png`](./charts/08_correlation_heatmap.png)

### 5. Consolidated Executive Dashboard
- **2×2 Multi-Panel Figure:** Integrates Category Bar Chart, Monthly Line Chart, Segment Pie Chart, and Top Sub-Categories.
  - File: [`charts/09_executive_dashboard.png`](./charts/09_executive_dashboard.png)

---

## 💻 Running Locally

### 1. Clone & Setup
```bash
git clone https://github.com/srujan1-creator/codomax-task3.git
cd codomax-task3
pip install -r requirements.txt
```

### 2. Run the End-to-End Analysis Pipeline
```bash
python main.py
```
This script audits data, cleans missing values, computes KPIs, and generates all charts into `charts/`.

### 3. Launch the Interactive Jupyter Notebook
```bash
jupyter notebook codomax_module3_data_analysis.ipynb
```

---

## 🧪 Automated Unit Testing

The repository includes comprehensive automated unit tests covering data cleaning, financial analytics, and chart generation:

```bash
python -m unittest discover -s tests
```

Output:
```
..............
----------------------------------------------------------------------
Ran 14 tests in 0.986s

OK
```

---

## 📋 Step-by-Step Google Colab Submission Guide

The Codomax submission portal requests a **Google Colab Link**. Follow these steps to submit:

### Step 1: Open Google Colab
1. Navigate to [colab.research.google.com](https://colab.research.google.com/) in your browser.
2. Sign in with your Google account.

### Step 2: Upload the Notebook
1. In the Colab pop-up window, select the **Upload** tab.
2. Click **Browse** and select `codomax_module3_data_analysis.ipynb` from this folder (`c:\codomax internship\codomax-task3\codomax_module3_data_analysis.ipynb`).
3. Alternatively, if pushed to GitHub, select the **GitHub** tab, enter your repository URL (`https://github.com/srujan1-creator/codomax-task3`), and click the notebook file!

### Step 3: Run the Notebook (Optional Verification)
1. In Colab, click **Runtime** in the top menu bar.
2. Select **Run all** (or press `Ctrl + F9`).
3. Verify that all cells execute cleanly with green checkmarks and all charts display inline.

### Step 4: Configure Shareable Permissions
1. In the top-right corner of Google Colab, click the **Share** button.
2. Under **General access**, change from **Restricted** to:
   > **"Anyone with the link can view"**
3. Click **Copy link**.

### Step 5: Submit in the Codomax Portal
1. Go to your Codomax Internship dashboard.
2. Under **Module 3: Data Analysis & Visualization**, click **Submit Link**.
3. Paste the copied Google Colab link into the input field and press submit!

---

## ✅ Submission Checklist
- [x] NumPy array vectorization, masking, and math operations implemented.
- [x] Pandas Series, DataFrames, and `.loc`/`.iloc` indexing demonstrated.
- [x] Sample dataset loaded and thoroughly explored with `.info()`, `.describe()`, and `.head()`.
- [x] Data cleaning performed (missing value imputation, deduplication, string sanitization).
- [x] Outliers analyzed using the IQR rule.
- [x] In-depth analysis performed with `groupby`, aggregations, pivot tables, and correlation matrix.
- [x] Bar charts created using Matplotlib.
- [x] Line charts created using Matplotlib.
- [x] Pie charts and Donut charts created using Matplotlib.
- [x] Consolidated Executive Dashboard generated.
- [x] Self-contained Google Colab Notebook (`codomax_module3_data_analysis.ipynb`) built and pre-rendered.
- [x] 14/14 automated unit tests passing.
- [x] Step-by-step submission instructions documented.
