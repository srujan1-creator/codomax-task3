"""
Data Cleaner Module
Codomax Internship — Module 3: Data Analysis & Visualization
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd


class DataCleaner:
    """
    Performs end-to-end data auditing, cleaning, transformation,
    and outlier treatment on raw tabular datasets.
    """

    def __init__(self, df: pd.DataFrame):
        self.raw_df = df.copy()
        self.df = df.copy()
        self.audit_log: Dict[str, Any] = {}

    def audit_raw_data(self) -> Dict[str, Any]:
        """Audits missing values, duplicates, and column types."""
        audit = {
            "initial_rows": len(self.df),
            "initial_columns": len(self.df.columns),
            "missing_values": self.df.isna().sum().to_dict(),
            "total_missing": int(self.df.isna().sum().sum()),
            "duplicate_rows": int(self.df.duplicated().sum()),
            "dtypes": {col: str(dtype) for col, dtype in self.df.dtypes.items()}
        }
        self.audit_log["audit"] = audit
        return audit

    def remove_duplicates(self) -> int:
        """Finds and drops duplicate rows."""
        initial = len(self.df)
        self.df = self.df.drop_duplicates().reset_index(drop=True)
        dropped = initial - len(self.df)
        self.audit_log["duplicates_removed"] = dropped
        return dropped

    def strip_whitespace(self) -> None:
        """Strips leading and trailing whitespace from string/object columns."""
        str_cols = self.df.select_dtypes(include=["object", "string", str]).columns
        for col in str_cols:
            self.df[col] = self.df[col].astype(str).str.strip()
            # Restore np.nan if string was 'nan'
            self.df[col] = self.df[col].replace("nan", np.nan)
        self.audit_log["whitespace_stripped_cols"] = list(str_cols)

    def handle_missing_values(self) -> Dict[str, Any]:
        """
        Strategically imputes or cleans missing values:
        - Numerical columns: Median imputation
        - Categorical columns: Mode (most frequent) imputation
        """
        imputation_record = {}
        for col in self.df.columns:
            null_count = self.df[col].isna().sum()
            if null_count > 0:
                if pd.api.types.is_numeric_dtype(self.df[col]):
                    median_val = self.df[col].median()
                    self.df[col] = self.df[col].fillna(median_val)
                    imputation_record[col] = {"strategy": "median", "value": round(float(median_val), 2), "count": int(null_count)}
                else:
                    mode_val = self.df[col].mode()[0]
                    self.df[col] = self.df[col].fillna(mode_val)
                    imputation_record[col] = {"strategy": "mode", "value": mode_val, "count": int(null_count)}
        self.audit_log["imputations"] = imputation_record
        return imputation_record

    def transform_datatypes(self) -> None:
        """Converts date strings to datetime objects and derives temporal features."""
        if "Order_Date" in self.df.columns:
            self.df["Order_Date"] = pd.to_datetime(self.df["Order_Date"])
            self.df["Month"] = self.df["Order_Date"].dt.month
            self.df["Month_Name"] = self.df["Order_Date"].dt.strftime("%b")
            self.df["Quarter"] = self.df["Order_Date"].dt.quarter
            self.audit_log["date_converted"] = True

    def detect_outliers_iqr(self, column: str) -> Tuple[pd.Series, float, float]:
        """
        Identifies outliers using the Interquartile Range (IQR) rule:
        Bounds = [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]
        """
        if column not in self.df.columns or not pd.api.types.is_numeric_dtype(self.df[column]):
            raise ValueError(f"Column '{column}' is not a numeric column.")

        q25 = np.percentile(self.df[column], 25)
        q75 = np.percentile(self.df[column], 75)
        iqr = q75 - q25
        lower_bound = q25 - 1.5 * iqr
        upper_bound = q75 + 1.5 * iqr

        outlier_mask = (self.df[column] < lower_bound) | (self.df[column] > upper_bound)
        return outlier_mask, lower_bound, upper_bound

    def run_pipeline(self) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """Executes full cleaning pipeline in canonical sequence."""
        self.audit_raw_data()
        self.strip_whitespace()
        self.remove_duplicates()
        self.handle_missing_values()
        self.transform_datatypes()
        
        self.audit_log["final_rows"] = len(self.df)
        self.audit_log["final_columns"] = len(self.df.columns)
        self.audit_log["remaining_nulls"] = int(self.df.isna().sum().sum())

        return self.df, self.audit_log
