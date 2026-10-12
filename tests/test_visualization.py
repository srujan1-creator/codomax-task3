"""
Unit Tests for Visualization Module
"""

import os
import unittest
import pandas as pd
from src.data_visualizer import DataVisualizer


class TestDataVisualizer(unittest.TestCase):

    def setUp(self):
        self.df = pd.DataFrame({
            "Order_ID": [f"ORD-{i}" for i in range(12)],
            "Category": ["Technology", "Furniture", "Office Supplies"] * 4,
            "Sub_Category": ["Phones", "Chairs", "Paper"] * 4,
            "Sales": [500.0, 300.0, 100.0] * 4,
            "Profit": [120.0, 40.0, 30.0] * 4,
            "Quantity": [2, 1, 4] * 4,
            "Discount": [0.05, 0.1, 0.0] * 4,
            "Customer_Rating": [4.0, 3.5, 4.5] * 4,
            "Region": ["North", "South", "East", "West"] * 3,
            "Segment": ["Consumer", "Corporate", "Home Office"] * 4,
            "Payment_Method": ["Credit Card", "PayPal", "UPI", "Bank Transfer"] * 3,
            "Month": [i + 1 for i in range(12)],
            "Month_Name": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        })
        self.temp_charts_dir = os.path.join(os.path.dirname(__file__), "temp_charts")
        self.visualizer = DataVisualizer(self.df, output_dir=self.temp_charts_dir)

    def tearDown(self):
        # Clean up temporary test charts
        if os.path.exists(self.temp_charts_dir):
            for f in os.listdir(self.temp_charts_dir):
                os.remove(os.path.join(self.temp_charts_dir, f))
            os.rmdir(self.temp_charts_dir)

    def test_bar_chart_generation(self):
        p = self.visualizer.plot_bar_category_sales_profit("test_bar.png")
        self.assertTrue(os.path.exists(p))
        self.assertGreater(os.path.getsize(p), 1000)

    def test_line_chart_generation(self):
        p = self.visualizer.plot_line_monthly_trends("test_line.png")
        self.assertTrue(os.path.exists(p))
        self.assertGreater(os.path.getsize(p), 1000)

    def test_pie_chart_generation(self):
        p = self.visualizer.plot_pie_customer_segments("test_pie.png")
        self.assertTrue(os.path.exists(p))
        self.assertGreater(os.path.getsize(p), 1000)

    def test_dashboard_generation(self):
        p = self.visualizer.plot_executive_dashboard("test_dashboard.png")
        self.assertTrue(os.path.exists(p))
        self.assertGreater(os.path.getsize(p), 1000)


if __name__ == "__main__":
    unittest.main()
