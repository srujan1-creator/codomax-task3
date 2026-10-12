"""
Data Analyzer Module
Codomax Internship — Module 3: Data Analysis & Visualization
"""

from typing import Dict, Any
import numpy as np
import pandas as pd


class DataAnalyzer:
    """
    Performs analytical computations, statistical aggregations,
    vectorized KPI calculations, and multidimensional summaries.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def calculate_kpis(self) -> Dict[str, float]:
        """Calculates core business executive KPIs using NumPy vectorization."""
        total_sales = float(np.sum(self.df["Sales"].to_numpy()))
        total_profit = float(np.sum(self.df["Profit"].to_numpy()))
        total_quantity = int(np.sum(self.df["Quantity"].to_numpy()))
        profit_margin = float((total_profit / total_sales * 100) if total_sales > 0 else 0.0)
        avg_order_value = float(np.mean(self.df["Sales"].to_numpy()))
        median_sales = float(np.median(self.df["Sales"].to_numpy()))
        std_sales = float(np.std(self.df["Sales"].to_numpy()))
        avg_rating = float(np.mean(self.df["Customer_Rating"].to_numpy()))

        return {
            "total_sales": round(total_sales, 2),
            "total_profit": round(total_profit, 2),
            "profit_margin_pct": round(profit_margin, 2),
            "total_units_sold": total_quantity,
            "avg_order_value": round(avg_order_value, 2),
            "median_order_value": round(median_sales, 2),
            "sales_std_dev": round(std_sales, 2),
            "avg_customer_rating": round(avg_rating, 2),
            "total_orders": len(self.df)
        }

    def category_performance(self) -> pd.DataFrame:
        """Aggregates metrics by Product Category."""
        cat_df = self.df.groupby("Category").agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Avg_Sales=("Sales", "mean"),
            Units_Sold=("Quantity", "sum"),
            Order_Count=("Order_ID", "count")
        ).reset_index()
        cat_df["Profit_Margin_Pct"] = (cat_df["Total_Profit"] / cat_df["Total_Sales"] * 100).round(2)
        cat_df["Total_Sales"] = cat_df["Total_Sales"].round(2)
        cat_df["Total_Profit"] = cat_df["Total_Profit"].round(2)
        cat_df["Avg_Sales"] = cat_df["Avg_Sales"].round(2)
        return cat_df.sort_values(by="Total_Sales", ascending=False)

    def subcategory_performance(self) -> pd.DataFrame:
        """Aggregates metrics by Sub-Category."""
        sub_df = self.df.groupby(["Category", "Sub_Category"]).agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Avg_Discount=("Discount", "mean"),
            Order_Count=("Order_ID", "count")
        ).reset_index()
        sub_df["Total_Sales"] = sub_df["Total_Sales"].round(2)
        sub_df["Total_Profit"] = sub_df["Total_Profit"].round(2)
        sub_df["Avg_Discount"] = (sub_df["Avg_Discount"] * 100).round(1)
        return sub_df.sort_values(by="Total_Sales", ascending=False)

    def monthly_trend(self) -> pd.DataFrame:
        """Computes chronological monthly trend of Sales, Profit, and Volume."""
        if "Month" not in self.df.columns and "Order_Date" in self.df.columns:
            self.df["Month"] = pd.to_datetime(self.df["Order_Date"]).dt.month
            self.df["Month_Name"] = pd.to_datetime(self.df["Order_Date"]).dt.strftime("%b")

        monthly = self.df.groupby(["Month", "Month_Name"]).agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Total_Orders=("Order_ID", "count")
        ).reset_index().sort_values(by="Month")

        monthly["Total_Sales"] = monthly["Total_Sales"].round(2)
        monthly["Total_Profit"] = monthly["Total_Profit"].round(2)
        return monthly

    def regional_performance(self) -> pd.DataFrame:
        """Computes regional sales, profit, and average margin."""
        region_df = self.df.groupby("Region").agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Order_Count=("Order_ID", "count"),
            Avg_Rating=("Customer_Rating", "mean")
        ).reset_index()
        region_df["Profit_Margin_Pct"] = (region_df["Total_Profit"] / region_df["Total_Sales"] * 100).round(2)
        region_df["Total_Sales"] = region_df["Total_Sales"].round(2)
        region_df["Total_Profit"] = region_df["Total_Profit"].round(2)
        region_df["Avg_Rating"] = region_df["Avg_Rating"].round(2)
        return region_df.sort_values(by="Total_Sales", ascending=False)

    def segment_distribution(self) -> pd.DataFrame:
        """Calculates customer segment revenue and order volume distribution."""
        seg_df = self.df.groupby("Segment").agg(
            Total_Sales=("Sales", "sum"),
            Total_Profit=("Profit", "sum"),
            Order_Count=("Order_ID", "count")
        ).reset_index()
        seg_df["Sales_Share_Pct"] = (seg_df["Total_Sales"] / seg_df["Total_Sales"].sum() * 100).round(2)
        return seg_df.sort_values(by="Total_Sales", ascending=False)

    def payment_method_distribution(self) -> pd.DataFrame:
        """Calculates revenue and frequency by payment method."""
        pay_df = self.df.groupby("Payment_Method").agg(
            Total_Sales=("Sales", "sum"),
            Order_Count=("Order_ID", "count")
        ).reset_index()
        pay_df["Share_Pct"] = (pay_df["Total_Sales"] / pay_df["Total_Sales"].sum() * 100).round(2)
        return pay_df.sort_values(by="Total_Sales", ascending=False)

    def regional_category_pivot(self) -> pd.DataFrame:
        """Generates cross-tabulation pivot table of Regional Sales by Category."""
        pivot = pd.pivot_table(
            self.df,
            values="Sales",
            index="Region",
            columns="Category",
            aggfunc="sum",
            fill_value=0
        ).round(2)
        return pivot

    def correlation_matrix(self) -> pd.DataFrame:
        """Calculates Pearson correlation matrix for numeric features."""
        num_cols = ["Unit_Price", "Quantity", "Discount", "Sales", "Profit", "Customer_Rating"]
        available_cols = [c for c in num_cols if c in self.df.columns]
        return self.df[available_cols].corr().round(3)
