"""
Unit Tests for Data Analysis Module
"""

import unittest
import pandas as pd
from src.data_analyzer import DataAnalyzer


class TestDataAnalyzer(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Order_ID": ["ORD-1", "ORD-2", "ORD-3", "ORD-4"],
            "Category": ["Technology", "Technology", "Furniture", "Office Supplies"],
            "Sub_Category": ["Phones", "Laptops", "Chairs", "Paper"],
            "Sales": [1000.0, 500.0, 300.0, 200.0],
            "Profit": [250.0, 100.0, 30.0, 80.0],
            "Quantity": [2, 1, 3, 4],
            "Discount": [0.05, 0.10, 0.0, 0.20],
            "Customer_Rating": [4.0, 5.0, 3.0, 4.0],
            "Region": ["North", "South", "North", "East"],
            "Segment": ["Consumer", "Corporate", "Consumer", "Home Office"],
            "Payment_Method": ["Credit Card", "PayPal", "Credit Card", "UPI"],
            "Month": [1, 2, 3, 4],
            "Month_Name": ["Jan", "Feb", "Mar", "Apr"]
        })
        self.analyzer = DataAnalyzer(self.df)

    def test_calculate_kpis(self):
        kpis = self.analyzer.calculate_kpis()
        self.assertEqual(kpis["total_sales"], 2000.0)
        self.assertEqual(kpis["total_profit"], 460.0)
        self.assertEqual(kpis["total_units_sold"], 10)
        self.assertEqual(kpis["total_orders"], 4)
        self.assertAlmostEqual(kpis["profit_margin_pct"], 23.0)

    def test_category_performance(self):
        cat_df = self.analyzer.category_performance()
        self.assertEqual(len(cat_df), 3)
        tech_row = cat_df[cat_df["Category"] == "Technology"].iloc[0]
        self.assertEqual(tech_row["Total_Sales"], 1500.0)
        self.assertEqual(tech_row["Total_Profit"], 350.0)

    def test_regional_performance(self):
        reg_df = self.analyzer.regional_performance()
        self.assertIn("Region", reg_df.columns)
        self.assertIn("Profit_Margin_Pct", reg_df.columns)

    def test_segment_distribution(self):
        seg_df = self.analyzer.segment_distribution()
        self.assertEqual(seg_df["Sales_Share_Pct"].sum(), 100.0)

    def test_correlation_matrix(self):
        corr = self.analyzer.correlation_matrix()
        self.assertIn("Sales", corr.columns)
        self.assertIn("Profit", corr.columns)
        self.assertEqual(corr.loc["Sales", "Sales"], 1.0)


if __name__ == "__main__":
    unittest.main()
