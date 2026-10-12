"""
Unit Tests for Data Cleaning Module
"""

import unittest
import numpy as np
import pandas as pd
from src.data_cleaner import DataCleaner


class TestDataCleaner(unittest.TestCase):

    def setUp(self):
        # Create a tiny mock dataframe with known defects
        self.raw_data = pd.DataFrame({
            "Order_ID": ["ORD-1", "ORD-2", "ORD-3", "ORD-3"],  # ORD-3 is duplicate
            "Category": [" Tech ", "Furniture", " Tech ", " Tech "],  # Trailing whitespace
            "Sales": [100.0, np.nan, 300.0, 300.0],  # 1 null
            "Order_Date": ["2023-01-01", "2023-02-01", "2023-03-01", "2023-03-01"],
            "Customer_Rating": [4.0, np.nan, 5.0, 5.0]
        })
        self.cleaner = DataCleaner(self.raw_data)

    def test_audit_raw_data(self):
        audit = self.cleaner.audit_raw_data()
        self.assertEqual(audit["initial_rows"], 4)
        self.assertEqual(audit["duplicate_rows"], 1)
        self.assertEqual(audit["total_missing"], 2)

    def test_strip_whitespace(self):
        self.cleaner.strip_whitespace()
        self.assertEqual(self.cleaner.df["Category"].iloc[0], "Tech")

    def test_remove_duplicates(self):
        dropped = self.cleaner.remove_duplicates()
        self.assertEqual(dropped, 1)
        self.assertEqual(len(self.cleaner.df), 3)

    def test_handle_missing_values(self):
        self.cleaner.remove_duplicates()
        imputations = self.cleaner.handle_missing_values()
        self.assertIn("Sales", imputations)
        self.assertEqual(self.cleaner.df["Sales"].isna().sum(), 0)

    def test_run_pipeline(self):
        clean_df, audit = self.cleaner.run_pipeline()
        self.assertEqual(len(clean_df), 3)
        self.assertEqual(clean_df.isna().sum().sum(), 0)
        self.assertIn("Month", clean_df.columns)
        self.assertIn("Month_Name", clean_df.columns)


if __name__ == "__main__":
    unittest.main()
