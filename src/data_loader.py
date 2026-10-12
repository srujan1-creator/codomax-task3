"""
Data Loader & Dataset Generator Module
Codomax Internship — Module 3: Data Analysis & Visualization
"""

import os
import numpy as np
import pandas as pd


def generate_ecommerce_dataset(num_records: int = 1200, random_state: int = 42) -> pd.DataFrame:
    """
    Generates a realistic, multifaceted E-commerce dataset with intentional
    real-world quirks (missing values, duplicates, edge cases) for demonstration
    of data exploration, data cleaning, statistical analysis, and visualization.
    """
    np.random.seed(random_state)

    categories = {
        "Technology": ["Phones", "Laptops", "Accessories", "Printers"],
        "Furniture": ["Chairs", "Tables", "Bookcases", "Furnishings"],
        "Office Supplies": ["Paper", "Binders", "Storage", "Art", "Appliances"]
    }

    segments = ["Consumer", "Corporate", "Home Office"]
    regions = ["North", "South", "East", "West", "Central"]
    payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "UPI"]

    dates = pd.date_range(start="2023-01-01", end="2023-12-31", periods=num_records)
    
    rows = []
    category_keys = list(categories.keys())

    for i in range(num_records):
        order_id = f"ORD-{2023000 + i}"
        customer_id = f"CUST-{np.random.randint(1000, 1400)}"
        order_date = dates[i].strftime("%Y-%m-%d")
        category = np.random.choice(category_keys, p=[0.35, 0.30, 0.35])
        sub_category = np.random.choice(categories[category])
        segment = np.random.choice(segments, p=[0.50, 0.30, 0.20])
        region = np.random.choice(regions, p=[0.25, 0.20, 0.22, 0.20, 0.13])

        # Realistic price base
        if category == "Technology":
            unit_price = float(np.random.uniform(150, 1200))
            cost_ratio = np.random.uniform(0.60, 0.75)
        elif category == "Furniture":
            unit_price = float(np.random.uniform(50, 600))
            cost_ratio = np.random.uniform(0.70, 0.85)
        else:
            unit_price = float(np.random.uniform(10, 150))
            cost_ratio = np.random.uniform(0.45, 0.65)

        quantity = int(np.random.choice([1, 2, 3, 4, 5, 6, 8, 10], p=[0.35, 0.25, 0.15, 0.10, 0.07, 0.04, 0.02, 0.02]))
        discount = float(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20, 0.30], p=[0.40, 0.20, 0.15, 0.12, 0.08, 0.05]))
        
        gross_sales = unit_price * quantity
        sales = round(gross_sales * (1.0 - discount), 2)
        cost = gross_sales * cost_ratio
        profit = round(sales - cost, 2)
        
        payment = np.random.choice(payment_methods, p=[0.45, 0.25, 0.18, 0.12])
        rating = float(np.random.choice([1.0, 2.0, 3.0, 4.0, 5.0], p=[0.05, 0.08, 0.22, 0.40, 0.25]))

        rows.append({
            "Order_ID": order_id,
            "Order_Date": order_date,
            "Customer_ID": customer_id,
            "Segment": segment,
            "Region": region,
            "Category": category,
            "Sub_Category": sub_category,
            "Unit_Price": round(unit_price, 2),
            "Quantity": quantity,
            "Discount": discount,
            "Sales": sales,
            "Profit": profit,
            "Payment_Method": payment,
            "Customer_Rating": rating
        })

    df = pd.DataFrame(rows)

    # Introduce intentional realistic anomalies for data cleaning demonstrations:
    # 1. Missing values (~3% in Customer_Rating, ~2% in Payment_Method, ~1% in Discount)
    null_rating_idx = np.random.choice(df.index, size=int(num_records * 0.03), replace=False)
    null_payment_idx = np.random.choice(df.index, size=int(num_records * 0.02), replace=False)
    null_discount_idx = np.random.choice(df.index, size=int(num_records * 0.015), replace=False)

    df.loc[null_rating_idx, "Customer_Rating"] = np.nan
    df.loc[null_payment_idx, "Payment_Method"] = np.nan
    df.loc[null_discount_idx, "Discount"] = np.nan

    # 2. Add a few duplicate records (5 duplicates)
    dup_indices = np.random.choice(df.index, size=5, replace=False)
    duplicates = df.loc[dup_indices].copy()
    df = pd.concat([df, duplicates], ignore_index=True)

    # 3. Add whitespace quirks in categorical column (e.g. ' Technology ')
    ws_indices = np.random.choice(df.index, size=8, replace=False)
    df.loc[ws_indices, "Category"] = df.loc[ws_indices, "Category"] + " "

    return df


def load_dataset(csv_path: str = None) -> pd.DataFrame:
    """
    Loads dataset from given CSV file or falls back to synthetic generation.
    """
    if csv_path and os.path.exists(csv_path):
        return pd.read_csv(csv_path)
    
    # Default path relative to project
    default_path = os.path.join(os.path.dirname(__file__), "..", "data", "ecommerce_sales_dataset.csv")
    if os.path.exists(default_path):
        return pd.read_csv(default_path)
    
    # Generate fresh if not found
    return generate_ecommerce_dataset()
