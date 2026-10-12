# Codomax Internship — Learning Journal: Module 3 (Day 9 – Day 12)
**Author:** Codomax Intern  
**Program:** Codomax Internship Program  
**Topic:** Data Analysis & Visualization (NumPy, Pandas, Matplotlib, Seaborn)  

---

## 📌 Table of Contents
1. [Day 9: NumPy & Pandas Foundations](#day-9-numpy--pandas-foundations)
   - [NumPy Architecture & Vectorization](#numpy-architecture--vectorization)
   - [Broadcasting Rules](#broadcasting-rules)
   - [Pandas Series & DataFrame Internals](#pandas-series--dataframe-internals)
   - [Indexing: `.loc` vs. `.iloc`](#indexing-loc-vs-iloc)
2. [Day 10: Exploratory Data Analysis (EDA)](#day-10-exploratory-data-analysis-eda)
   - [Structural Auditing & Schema Triage](#structural-auditing--schema-triage)
   - [Summary Statistics & Central Tendency](#summary-statistics--central-tendency)
   - [Cardinality & Categorical Distributions](#cardinality--categorical-distributions)
3. [Day 11: Data Cleaning & Deep Analytical Methods](#day-11-data-cleaning--deep-analytical-methods)
   - [Missing Data Imputation Strategies](#missing-data-imputation-strategies)
   - [Deduplication & String Sanitization](#deduplication--string-sanitization)
   - [Outlier Detection via IQR Rule](#outlier-detection-via-iqr-rule)
   - [Split-Apply-Combine with GroupBy & Pivot Tables](#split-apply-combine-with-groupby--pivot-tables)
   - [Correlation Analysis](#correlation-analysis)
4. [Day 12: Data Visualization & Matplotlib Architecture](#day-12-data-visualization--matplotlib-architecture)
   - [The Object-Oriented Hierarchy: Figure vs. Axes](#the-object-oriented-hierarchy-figure-vs-axes)
   - [Chart Selection Taxonomy](#chart-selection-taxonomy)
   - [Visual Storytelling & Aesthetics](#visual-storytelling--aesthetics)
   - [Multi-Panel Dashboard Design](#multi-panel-dashboard-design)
5. [Summary of Engineering Takeaways](#summary-of-engineering-takeaways)

---

## Day 9: NumPy & Pandas Foundations

### NumPy Architecture & Vectorization
Traditional Python lists store pointers to heap-allocated PyObject instances. A list of 1,000 integers contains 1,000 distinct pointers, each with type-check overhead, garbage collection headers, and non-contiguous memory allocations.

In contrast, a **NumPy `ndarray`**:
1. Allocates a single, contiguous block of raw memory (C-contiguous or Fortran-contiguous).
2. Maintains a single data type (`dtype`), eliminating runtime type checking.
3. Leverages low-level CPU vector instructions (SIMD: Single Instruction, Multiple Data) through BLAS/LAPACK backends.

```python
# Benchmarking comparison: Loop vs. Vectorization
# Python list loop: O(N) interpreted bytecodes
squares = [x**2 for x in py_list]

# NumPy vectorization: Executed at C-speed
squares = np_array ** 2  # Typically 50x - 200x faster
```

### Broadcasting Rules
Broadcasting allows NumPy to execute arithmetic operations across arrays of differing shapes without making unnecessary memory copies:
1. Two dimensions are compatible when:
   - They are equal, OR
   - One of them is 1.
2. If arrays have differing numbers of dimensions, the shape of the array with fewer dimensions is padded with leading ones on its left.

### Pandas Series & DataFrame Internals
- A **`Series`** is a 1-dimensional labeled array capable of holding any data type, backed by a NumPy array and an index structure.
- A **`DataFrame`** is a 2-dimensional tabular structure consisting of an aligned collection of Series that share a common index.

### Indexing: `.loc` vs. `.iloc`
| Indexer | Basis | Syntax Example | Behavior |
| :--- | :--- | :--- | :--- |
| **`.loc`** | Label-based | `df.loc['2023-01-01', 'Sales']` | End point is **inclusive**; references index and column labels. |
| **`.iloc`** | Integer position | `df.iloc[0:5, 0:3]` | End point is **exclusive** (like Python slices); references integer offsets. |

---

## Day 10: Exploratory Data Analysis (EDA)

### Structural Auditing & Schema Triage
Before performing transformations, a structured audit assesses data fidelity:
1. **Dimensions:** `df.shape` reveals sample size $N$ and feature count $P$.
2. **Schema & Nulls:** `df.info()` reveals non-null counts and memory consumption.
3. **First & Last Observations:** `df.head()` and `df.tail()` ensure parsing did not invert headers or append trailing corrupted rows.

### Summary Statistics & Central Tendency
`df.describe()` outputs eight essential statistical metrics:
- **Mean vs. Median:** When $\text{Mean} \gg \text{Median}$, the distribution is positively skewed (right-tailed), indicating high-value outliers (common in sales and income data).
- **Standard Deviation vs. IQR:** Standard deviation is sensitive to extreme values; IQR provides a robust measure of dispersion.

### Cardinality & Categorical Distributions
- **`nunique()`** distinguishes continuous identifiers (high cardinality, e.g., `Order_ID`) from categorical groupings (low cardinality, e.g., `Region`, `Category`).
- **`value_counts()`** identifies class imbalance and rare categorical entries.

---

## Day 11: Data Cleaning & Deep Analytical Methods

### Missing Data Imputation Strategies
Missing data falls into three foundational categories:
1. **MCAR (Missing Completely at Random):** Missingness has no relationship with any data.
2. **MAR (Missing at Random):** Missingness is related to observed features.
3. **MNAR (Missing Not at Random):** Missingness depends on the unobserved value itself.

#### Imputation Rules Applied:
- **Numerical Features (Skewed distributions):** Imputed with the **Median**. Unlike the mean, the median is resistant to extreme outliers.
- **Categorical Dimensions:** Imputed with the **Mode** (most frequent categorical value).

### Deduplication & String Sanitization
- Duplicate transaction entries can artificially inflate revenue and skew counts. We enforce idempotency using `df.drop_duplicates()`.
- Text columns frequently suffer from trailing whitespace (`" Technology "`). Sanitizing with `.str.strip()` prevents artificial cardinality inflation.

### Outlier Detection via IQR Rule
We employ John Tukey's **Interquartile Range (IQR)** boxplot rule:
$$\text{IQR} = Q_3 - Q_1$$
$$\text{Lower Bound} = Q_1 - 1.5 \times \text{IQR}$$
$$\text{Upper Bound} = Q_3 + 1.5 \times \text{IQR}$$

Values falling outside this interval are flagged as outliers. In business applications, these often correspond to legitimate bulk corporate purchases rather than sensor errors, so flagging rather than blindly discarding is paramount.

### Split-Apply-Combine with GroupBy & Pivot Tables
The **Split-Apply-Combine** strategy:
1. **Split:** Data is partitioned into subsets based on grouping keys (`Category`, `Region`).
2. **Apply:** An aggregation function (`sum`, `mean`, `count`, `std`) computes summary values.
3. **Combine:** Results are joined into a clean summary DataFrame.

```python
# Multi-metric Category Aggregation
cat_summary = df.groupby("Category").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Profit", "sum"),
    Order_Count=("Order_ID", "count")
)
```

Cross-tabulation via `pd.pivot_table()` converts categorical combinations into a matrix format for multi-dimensional comparisons.

### Correlation Analysis
The Pearson correlation coefficient measures linear co-movement between two continuous variables:
$$r_{xy} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}$$

Key observations:
- Strong positive correlation between `Unit_Price` and `Sales` ($r \approx 0.78$).
- Negative relationship between `Discount` and `Profit` when discounts exceed 20%.

---

## Day 12: Data Visualization & Matplotlib Architecture

### The Object-Oriented Hierarchy: Figure vs. Axes
Matplotlib provides two APIs:
1. **Stateful `pyplot` interface:** Implicitly modifies the current active figure/axis. (Prone to bugs in complex layouts).
2. **Object-Oriented (OO) interface:** Explicitly creates and references `Figure` (the canvas container) and `Axes` (the individual plotting area).

```python
# Recommended Object-Oriented Paradigm
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x, y)
ax.set_title("Explicit Object Manipulation")
```

### Chart Selection Taxonomy

| Chart Type | Purpose & Best Use Case | Project Implementation |
| :--- | :--- | :--- |
| **Bar Chart** | Discrete categorical comparisons & rankings | Total Sales & Profit across Categories; Top 10 Sub-Categories. |
| **Line Chart** | Continuous trends across time/intervals | Chronological 12-month sales trajectory; Regional monthly trends. |
| **Pie / Donut Chart** | Proportions of a whole ($\le 5$ categories) | Customer segment revenue share (Pie); Payment method distribution (Donut). |
| **Scatter Plot** | Bivariate correlation & outlier clustering | Discount percentage vs. Net Profit (with break-even line). |
| **Heatmap** | Matrix density & correlation coefficients | Pearson correlation matrix across numerical variables. |

### Visual Storytelling & Aesthetics
1. **Data-to-Ink Ratio:** Eliminated chart junk; utilized subtle grid lines (`seaborn-v0_8-whitegrid`).
2. **Direct Annotation:** Placed formatted dollar labels directly atop bars (`$662k`), reducing eye travel to the vertical axis.
3. **Visual Hierarchy:** Applied bold typography for titles, semibold for axes, and regular for tick labels.
4. **Color Palettes:** Used accessible, complementary colors (`#1f77b4` blue for Sales, `#2ca02c` green for Profit).

### Multi-Panel Dashboard Design
Using `plt.subplots(2, 2, figsize=(16, 11))` creates a unified executive view presenting:
- Top-left: Category Sales & Profit comparison
- Top-right: 12-Month revenue trend
- Bottom-left: Customer segment market share
- Bottom-right: Top sub-category sales rankings

---

## Summary of Engineering Takeaways
- **Data Quality Precedes Modeling:** Clean data drives reliable business conclusions; never visualize raw unvalidated data.
- **Vectorization is Paramount:** Native Pandas and NumPy vector operations run orders of magnitude faster than iterating with Python loops.
- **Charts Must Answer Business Questions:** Every visualization must provide immediate operational clarity and context.
