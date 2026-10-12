"""
Data Visualizer Module
Codomax Internship — Module 3: Data Analysis & Visualization
Uses Matplotlib and Seaborn to generate professional, publication-quality visualizations.
"""

import os
from typing import Optional
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns


# Set global clean aesthetic
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10
plt.rcParams["axes.titlesize"] = 12
plt.rcParams["axes.labelsize"] = 10


class DataVisualizer:
    """
    Renders and exports data visualizations using Matplotlib & Seaborn.
    """

    def __init__(self, df: pd.DataFrame, output_dir: Optional[str] = None):
        self.df = df
        self.output_dir = output_dir or os.path.join(os.path.dirname(__file__), "..", "charts")
        os.makedirs(self.output_dir, exist_ok=True)
        # Palette definitions
        self.colors = ["#2b5c8f", "#e06d53", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]

    def plot_bar_category_sales_profit(self, save_filename: str = "01_bar_chart_sales_profit_by_category.png") -> str:
        """
        Creates a grouped bar chart comparing Total Sales and Total Profit
        across product categories.
        """
        cat_summary = self.df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
        
        x = np.arange(len(cat_summary))
        width = 0.35

        fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
        
        rects1 = ax.bar(x - width/2, cat_summary["Sales"], width, label="Total Sales ($)", color="#1f77b4", edgecolor="black", alpha=0.9)
        rects2 = ax.bar(x + width/2, cat_summary["Profit"], width, label="Total Profit ($)", color="#2ca02c", edgecolor="black", alpha=0.9)

        ax.set_ylabel("USD ($)", fontweight="bold")
        ax.set_title("Total Sales & Profit by Product Category", fontsize=14, fontweight="bold", pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(cat_summary["Category"], fontweight="bold")
        ax.legend(frameon=True, facecolor="white", edgecolor="none")
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))

        # Add data labels
        for rect in rects1:
            height = rect.get_height()
            ax.annotate(f"${height:,.0f}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, fontweight="bold")
            
        for rect in rects2:
            height = rect.get_height()
            ax.annotate(f"${height:,.0f}",
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 4), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8, fontweight="bold")

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_bar_top_subcategories(self, save_filename: str = "02_bar_chart_top10_subcategories.png") -> str:
        """
        Creates a horizontal bar chart displaying top 10 Sub-Categories by Sales.
        """
        sub_summary = self.df.groupby("Sub_Category")["Sales"].sum().sort_values(ascending=True).tail(10)

        fig, ax = plt.subplots(figsize=(9, 5.5), dpi=150)
        bars = ax.barh(sub_summary.index, sub_summary.values, color="#3470a3", edgecolor="black", alpha=0.85)

        ax.set_xlabel("Total Sales ($)", fontweight="bold")
        ax.set_title("Top 10 Sub-Categories by Total Sales", fontsize=14, fontweight="bold", pad=15)
        ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))

        for bar in bars:
            width = bar.get_width()
            ax.annotate(f"${width:,.0f}",
                        xy=(width, bar.get_y() + bar.get_height() / 2),
                        xytext=(5, 0), textcoords="offset points",
                        ha="left", va="center", fontsize=8, fontweight="bold")

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_line_monthly_trends(self, save_filename: str = "03_line_chart_monthly_sales_trend.png") -> str:
        """
        Creates a chronological line chart showing monthly sales and profit trajectory.
        """
        monthly = self.df.groupby(["Month", "Month_Name"])[["Sales", "Profit"]].sum().reset_index().sort_values("Month")

        fig, ax = plt.subplots(figsize=(10, 5), dpi=150)

        ax.plot(monthly["Month_Name"], monthly["Sales"], marker="o", linewidth=2.5, color="#1f77b4", label="Monthly Sales ($)")
        ax.plot(monthly["Month_Name"], monthly["Profit"], marker="s", linewidth=2.5, color="#2ca02c", linestyle="--", label="Monthly Profit ($)")
        
        ax.fill_between(monthly["Month_Name"], monthly["Sales"], color="#1f77b4", alpha=0.1)

        ax.set_title("Monthly Sales & Profit Performance Trend (2023)", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Month", fontweight="bold")
        ax.set_ylabel("USD ($)", fontweight="bold")
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.legend(frameon=True, facecolor="white")

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_line_regional_trends(self, save_filename: str = "04_line_chart_regional_trends.png") -> str:
        """
        Creates a multi-line chart depicting monthly sales across regions.
        """
        pivot_monthly_reg = self.df.pivot_table(
            index="Month_Name",
            columns="Region",
            values="Sales",
            aggfunc="sum"
        )
        # Ensure chronological order
        months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        pivot_monthly_reg = pivot_monthly_reg.reindex([m for m in months_order if m in pivot_monthly_reg.index])

        fig, ax = plt.subplots(figsize=(10, 5.5), dpi=150)
        for col in pivot_monthly_reg.columns:
            ax.plot(pivot_monthly_reg.index, pivot_monthly_reg[col], marker="o", label=col, linewidth=2)

        ax.set_title("Monthly Revenue Trajectory by Geographic Region", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Month", fontweight="bold")
        ax.set_ylabel("Sales ($)", fontweight="bold")
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.legend(title="Region", bbox_to_anchor=(1.02, 1), loc="upper left")

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_pie_customer_segments(self, save_filename: str = "05_pie_chart_customer_segments.png") -> str:
        """
        Creates an exploded pie chart displaying revenue share by customer segment.
        """
        seg_summary = self.df.groupby("Segment")["Sales"].sum()
        explode = [0.05 if i == seg_summary.values.argmax() else 0 for i in range(len(seg_summary))]
        colors = ["#3282b8", "#0f4c75", "#bbe1fa"]

        fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
        wedges, texts, autotexts = ax.pie(
            seg_summary.values,
            labels=seg_summary.index,
            autopct="%1.1f%%",
            startangle=140,
            explode=explode,
            colors=colors,
            wedgeprops={"edgecolor": "white", "linewidth": 2},
            textprops={"fontsize": 10}
        )

        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")

        ax.set_title("Revenue Contribution by Customer Segment", fontsize=14, fontweight="bold", pad=15)

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_donut_payment_methods(self, save_filename: str = "06_donut_chart_payment_methods.png") -> str:
        """
        Creates a donut chart illustrating payment method adoption.
        """
        pay_summary = self.df.groupby("Payment_Method")["Sales"].sum().sort_values(ascending=False)
        colors = ["#2b5c8f", "#457b9d", "#a8dadc", "#e63946"]

        fig, ax = plt.subplots(figsize=(7, 6), dpi=150)
        wedges, texts, autotexts = ax.pie(
            pay_summary.values,
            labels=pay_summary.index,
            autopct="%1.1f%%",
            startangle=90,
            colors=colors,
            pctdistance=0.75,
            wedgeprops={"edgecolor": "white", "linewidth": 2}
        )

        # Draw inner white circle for donut hole
        centre_circle = plt.Circle((0, 0), 0.55, fc="white")
        fig.gca().add_artist(centre_circle)

        for autotext in autotexts:
            autotext.set_fontweight("bold")

        ax.set_title("Sales Share by Payment Method (Donut Chart)", fontsize=14, fontweight="bold", pad=15)

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_scatter_discount_profit(self, save_filename: str = "07_scatter_discount_vs_profit.png") -> str:
        """
        Creates a scatter plot showing relationship between Discount and Profit.
        """
        fig, ax = plt.subplots(figsize=(8.5, 5.5), dpi=150)
        scatter = ax.scatter(
            self.df["Discount"] * 100,
            self.df["Profit"],
            c=self.df["Sales"],
            cmap="viridis",
            alpha=0.65,
            edgecolors="none",
            s=40
        )
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label("Sales ($)", fontweight="bold")

        ax.axhline(0, color="red", linestyle="--", linewidth=1.2, alpha=0.8, label="Break-Even ($0 Profit)")
        ax.set_title("Impact of Discount Rate on Order Profitability", fontsize=14, fontweight="bold", pad=15)
        ax.set_xlabel("Discount Percentage (%)", fontweight="bold")
        ax.set_ylabel("Profit ($)", fontweight="bold")
        ax.legend()

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_correlation_heatmap(self, save_filename: str = "08_correlation_heatmap.png") -> str:
        """
        Renders a correlation matrix heatmap for numeric features.
        """
        num_cols = ["Unit_Price", "Quantity", "Discount", "Sales", "Profit", "Customer_Rating"]
        available_cols = [c for c in num_cols if c in self.df.columns]
        corr = self.df[available_cols].corr()

        fig, ax = plt.subplots(figsize=(7.5, 6), dpi=150)
        sns.heatmap(
            corr,
            annot=True,
            fmt=".2f",
            cmap="coolwarm",
            center=0,
            square=True,
            linewidths=1,
            cbar_kws={"shrink": 0.8},
            ax=ax
        )
        ax.set_title("Numeric Feature Correlation Matrix", fontsize=14, fontweight="bold", pad=15)

        plt.tight_layout()
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def plot_executive_dashboard(self, save_filename: str = "09_executive_dashboard.png") -> str:
        """
        Creates a 2x2 multi-panel Executive Dashboard combining:
        1. Category Sales & Profit Bar Chart
        2. Monthly Sales Trend Line Chart
        3. Customer Segment Share Pie Chart
        4. Top Sub-Categories Horizontal Bar Chart
        """
        fig, axs = plt.subplots(2, 2, figsize=(16, 11), dpi=150)
        fig.suptitle("Codomax Internship — Executive Data Analysis & Visualization Dashboard", fontsize=18, fontweight="bold", y=0.98)

        # 1. Bar Chart (Top Left)
        cat_summary = self.df.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
        x = np.arange(len(cat_summary))
        width = 0.35
        axs[0, 0].bar(x - width/2, cat_summary["Sales"], width, label="Sales ($)", color="#1f77b4", edgecolor="black")
        axs[0, 0].bar(x + width/2, cat_summary["Profit"], width, label="Profit ($)", color="#2ca02c", edgecolor="black")
        axs[0, 0].set_xticks(x)
        axs[0, 0].set_xticklabels(cat_summary["Category"], fontweight="bold")
        axs[0, 0].set_title("Sales & Profit by Category", fontweight="bold", fontsize=12)
        axs[0, 0].set_ylabel("USD ($)")
        axs[0, 0].yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        axs[0, 0].legend()

        # 2. Line Chart (Top Right)
        monthly = self.df.groupby(["Month", "Month_Name"])[["Sales", "Profit"]].sum().reset_index().sort_values("Month")
        axs[0, 1].plot(monthly["Month_Name"], monthly["Sales"], marker="o", color="#1f77b4", linewidth=2.5, label="Sales")
        axs[0, 1].plot(monthly["Month_Name"], monthly["Profit"], marker="s", color="#2ca02c", linestyle="--", linewidth=2.5, label="Profit")
        axs[0, 1].fill_between(monthly["Month_Name"], monthly["Sales"], color="#1f77b4", alpha=0.1)
        axs[0, 1].set_title("Monthly Trend (Sales & Profit)", fontweight="bold", fontsize=12)
        axs[0, 1].yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        axs[0, 1].legend()

        # 3. Pie Chart (Bottom Left)
        seg_summary = self.df.groupby("Segment")["Sales"].sum()
        colors = ["#3282b8", "#0f4c75", "#bbe1fa"]
        axs[1, 0].pie(
            seg_summary.values,
            labels=seg_summary.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            wedgeprops={"edgecolor": "white", "linewidth": 1.5}
        )
        axs[1, 0].set_title("Revenue Share by Customer Segment", fontweight="bold", fontsize=12)

        # 4. Horizontal Bar Chart (Bottom Right)
        sub_summary = self.df.groupby("Sub_Category")["Sales"].sum().sort_values().tail(7)
        axs[1, 1].barh(sub_summary.index, sub_summary.values, color="#3470a3", edgecolor="black")
        axs[1, 1].set_title("Top 7 Sub-Categories by Sales", fontweight="bold", fontsize=12)
        axs[1, 1].set_xlabel("Sales ($)")
        axs[1, 1].xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))

        plt.tight_layout(rect=[0, 0, 1, 0.95])
        save_path = os.path.join(self.output_dir, save_filename)
        plt.savefig(save_path, bbox_inches="tight")
        plt.close()
        return save_path

    def render_all(self) -> list:
        """Executes all chart generation routines and returns output file paths."""
        paths = [
            self.plot_bar_category_sales_profit(),
            self.plot_bar_top_subcategories(),
            self.plot_line_monthly_trends(),
            self.plot_line_regional_trends(),
            self.plot_pie_customer_segments(),
            self.plot_donut_payment_methods(),
            self.plot_scatter_discount_profit(),
            self.plot_correlation_heatmap(),
            self.plot_executive_dashboard()
        ]
        return paths
