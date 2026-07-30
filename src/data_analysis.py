import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("data/raw/01_fund_master.csv")

# Display first 5 rows
print("\n===== FIRST 5 ROWS =====")
print(df.head())

# Shape
print("\n===== SHAPE =====")
print(df.shape)

# Columns
print("\n===== COLUMN NAMES =====")
print(df.columns)

# Information
print("\n===== DATA INFO =====")
print(df.info())

# Missing Values
print("\n===== MISSING VALUES =====")
print(df.isnull().sum())

# Duplicate Rows
print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())

# Statistics
print("\n===== DESCRIBE =====")
print(df.describe())
print("\n========== KPI REPORT ==========")

# Total Schemes
print("Total Mutual Fund Schemes :", len(df))

# Total Fund Houses
print("Total Fund Houses :", df["fund_house"].nunique())

# Total Categories
print("Total Categories :", df["category"].nunique())

# Average Expense Ratio
print("Average Expense Ratio :", round(df["expense_ratio_pct"].mean(),2))

# Maximum Expense Ratio
print("Maximum Expense Ratio :", df["expense_ratio_pct"].max())

# Minimum Expense Ratio
print("Minimum Expense Ratio :", df["expense_ratio_pct"].min())

# Average SIP Amount
print("Average Minimum SIP :", round(df["min_sip_amount"].mean(),2))
# ==========================
# BAR CHART
# ==========================

category_count = df["category"].value_counts()

plt.figure(figsize=(8,5))
category_count.plot(kind="bar", color="skyblue")

plt.title("Number of Mutual Fund Schemes by Category")
plt.xlabel("Category")
plt.ylabel("Count")

plt.xticks(rotation=45)

plt.tight_layout()

# Save bar chart
plt.savefig("reports/category_bar_chart.png")

plt.close()


# ==========================
# PIE CHART
# ==========================

plt.figure(figsize=(7,7))

category_count.plot(
    kind="pie",
    autopct="%1.1f%%"
)

plt.title("Category Distribution")
plt.ylabel("")

# Save pie chart
plt.savefig("reports/category_pie_chart.png")

plt.close()


# ==========================
# SAVE CLEANED DATASET
# ==========================


df.to_csv(
    "data/processed/cleaned_fund_master.csv",
    index=False
)

print("\nCleaned dataset saved successfully.")
print("Bar chart saved in : reports/category_bar_chart.png")
print("Pie chart saved in : reports/category_pie_chart.png")
print("Processed CSV saved in : data/processed/cleaned_fund_master.csv")
