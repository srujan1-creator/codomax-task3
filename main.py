#!/usr/bin/env python3
"""
Main Execution Script for Codomax Internship — Module 3: Data Analysis & Visualization
Day 9 - Day 12 Deliverable Pipeline
"""

import os
import sys

# Ensure local imports resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_loader import load_dataset
from src.data_cleaner import DataCleaner
from src.data_analyzer import DataAnalyzer
from src.data_visualizer import DataVisualizer


def print_banner():
    banner = """
================================================================================
  CODOMAX INTERNSHIP -- MODULE 3: DATA ANALYSIS & VISUALIZATION (DAY 9 - 12)
  Deliverable: Google Colab Ready Notebook & End-to-End Analytics Pipeline
================================================================================
    """
    print(banner)


def main():
    print_banner()

    # Step 1: Load Raw Dataset
    print("[1/4] Loading E-Commerce Sales Dataset...")
    data_path = os.path.join(os.path.dirname(__file__), "data", "ecommerce_sales_dataset.csv")
    raw_df = load_dataset(data_path)
    print(f"      -> Loaded {len(raw_df)} records across {len(raw_df.columns)} columns.")

    # Step 2: Data Cleaning & Preprocessing
    print("\n[2/4] Auditing and Cleaning Data...")
    cleaner = DataCleaner(raw_df)
    clean_df, audit = cleaner.run_pipeline()
    
    print(f"      -> Duplicate rows removed: {audit.get('duplicates_removed', 0)}")
    print(f"      -> Imputations performed: {list(audit.get('imputations', {}).keys())}")
    print(f"      -> Final Clean Dataset Dimensions: {clean_df.shape[0]} rows x {clean_df.shape[1]} columns")

    # Save cleaned dataset
    clean_csv_path = os.path.join(os.path.dirname(__file__), "data", "cleaned_sales_dataset.csv")
    clean_df.to_csv(clean_csv_path, index=False)
    print(f"      -> Saved clean dataset to: {clean_csv_path}")

    # Step 3: Statistical Analysis & Business KPIs
    print("\n[3/4] Performing In-Depth Statistical & Financial Analysis...")
    analyzer = DataAnalyzer(clean_df)
    kpis = analyzer.calculate_kpis()

    print("\n" + "="*50)
    print("           EXECUTIVE KPI SUMMARY")
    print("="*50)
    print(f"  Total Revenue:           ${kpis['total_sales']:,.2f}")
    print(f"  Total Profit:            ${kpis['total_profit']:,.2f}")
    print(f"  Net Profit Margin:       {kpis['profit_margin_pct']}%")
    print(f"  Total Units Sold:        {kpis['total_units_sold']:,}")
    print(f"  Average Order Value:     ${kpis['avg_order_value']:,.2f}")
    print(f"  Median Order Value:      ${kpis['median_order_value']:,.2f}")
    print(f"  Average Customer Rating: {kpis['avg_customer_rating']} / 5.0")
    print("="*50 + "\n")

    print("--- Performance by Category ---")
    cat_perf = analyzer.category_performance()
    print(cat_perf.to_string(index=False))

    print("\n--- Performance by Region ---")
    reg_perf = analyzer.regional_performance()
    print(reg_perf.to_string(index=False))

    # Step 4: Data Visualization (Bar, Line, Pie, Donut, Dashboard)
    print("\n[4/4] Generating Publication-Quality Matplotlib Charts...")
    charts_dir = os.path.join(os.path.dirname(__file__), "charts")
    visualizer = DataVisualizer(clean_df, output_dir=charts_dir)
    rendered_paths = visualizer.render_all()

    print(f"      -> Successfully generated {len(rendered_paths)} charts in '{charts_dir}':")
    for path in rendered_paths:
        print(f"         [OK] {os.path.basename(path)}")

    print("\n" + "="*80)
    print("  Pipeline execution complete! All analyses and charts successfully rendered.")
    print("================================================================================\n")


if __name__ == "__main__":
    main()
