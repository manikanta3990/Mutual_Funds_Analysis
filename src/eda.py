import pandas as pd
import numpy as np

# ==========================================
# 1. LOAD DATASET
# ==========================================

df = pd.read_csv("data/raw/01_fund_master.csv")

print("===== FIRST 5 ROWS =====")
print(df.head())

print("\n===== SHAPE =====")
print(df.shape)

print("\n===== COLUMN NAMES =====")
print(df.columns)

print("\n===== DATA TYPES =====")
print(df.dtypes)


# ==========================================
# 2. MISSING VALUES
# ==========================================

print("\n===== MISSING VALUES =====")
print(df.isnull().sum())


# ==========================================
# 3. DUPLICATE ROWS
# ==========================================

print("\n===== DUPLICATE ROWS =====")
print(df.duplicated().sum())


# ==========================================
# 4. REMOVE DUPLICATES
# ==========================================

df = df.drop_duplicates()

print("\n===== SHAPE AFTER DUPLICATE REMOVAL =====")
print(df.shape)
# ==========================================
# 5. DATA VALIDATION
# ==========================================

print("\n===== DATA VALIDATION =====")

# Check duplicate AMFI codes
print("\nDuplicate AMFI codes:")
print(df["amfi_code"].duplicated().sum())

# Check negative expense ratios
print("\nNegative expense ratios:")
print((df["expense_ratio_pct"] < 0).sum())

# Check negative exit loads
print("\nNegative exit loads:")
print((df["exit_load_pct"] < 0).sum())

# Check negative SIP amounts
print("\nNegative SIP amounts:")
print((df["min_sip_amount"] < 0).sum())

# Check negative lumpsum amounts
print("\nNegative lumpsum amounts:")
print((df["min_lumpsum_amount"] < 0).sum())

# Convert launch date to datetime
df["launch_date"] = pd.to_datetime(
    df["launch_date"],
    errors="coerce"
)

# Check invalid dates
print("\nInvalid launch dates:")
print(df["launch_date"].isnull().sum())
# ==========================================
# 6. OUTLIER DETECTION USING IQR
# ==========================================

print("\n===== OUTLIER DETECTION =====")

numeric_columns = [
    "expense_ratio_pct",
    "exit_load_pct",
    "min_sip_amount",
    "min_lumpsum_amount"
]

for column in numeric_columns:

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_limit) |
        (df[column] > upper_limit)
    ]

    print(f"\nColumn: {column}")
    print(f"Q1: {Q1}")
    print(f"Q3: {Q3}")
    print(f"IQR: {IQR}")
    print(f"Lower Limit: {lower_limit}")
    print(f"Upper Limit: {upper_limit}")
    print(f"Number of Outliers: {len(outliers)}")
    # ==========================================
# 7. BASIC STATISTICS
# ==========================================

print("\n===== BASIC STATISTICS =====")

print(df.describe())


# ==========================================
# 8. CORRELATION ANALYSIS
# ==========================================

print("\n===== CORRELATION MATRIX =====")

numeric_columns = [
    "expense_ratio_pct",
    "exit_load_pct",
    "min_sip_amount",
    "min_lumpsum_amount"
]

correlation_matrix = df[numeric_columns].corr()

print(correlation_matrix)
# ==========================================
# 9. CATEGORY ANALYSIS
# ==========================================

print("\n===== SCHEMES BY CATEGORY =====")

category_count = df["category"].value_counts()

print(category_count)


# ==========================================
# 10. FUND HOUSE ANALYSIS
# ==========================================

print("\n===== SCHEMES BY FUND HOUSE =====")

fund_house_count = df["fund_house"].value_counts()

print(fund_house_count)


# ==========================================
# 11. RISK CATEGORY ANALYSIS
# ==========================================

print("\n===== RISK CATEGORY DISTRIBUTION =====")

risk_count = df["risk_category"].value_counts()

print(risk_count)


# ==========================================
# 12. LAUNCH YEAR ANALYSIS
# ==========================================

print("\n===== SCHEMES BY LAUNCH YEAR =====")

launch_year_count = (
    df["launch_date"]
    .dt.year
    .value_counts()
    .sort_index()
)

print(launch_year_count)
# ==========================================
# 13. VISUALIZATIONS
# ==========================================

import matplotlib.pyplot as plt
import os

os.makedirs("data/charts", exist_ok=True)


# ==========================================
# CHART 1: SCHEMES BY CATEGORY
# ==========================================

plt.figure(figsize=(8, 5))

category_count.plot(kind="bar")

plt.title("Number of Mutual Fund Schemes by Category")
plt.xlabel("Category")
plt.ylabel("Number of Schemes")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("data/charts/schemes_by_category.png")

plt.close()


# ==========================================
# CHART 2: RISK CATEGORY DISTRIBUTION
# ==========================================

plt.figure(figsize=(7, 5))

risk_count.plot(kind="bar")

plt.title("Mutual Fund Schemes by Risk Category")
plt.xlabel("Risk Category")
plt.ylabel("Number of Schemes")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("data/charts/risk_category_distribution.png")

plt.close()


# ==========================================
# CHART 3: SCHEMES BY LAUNCH YEAR
# ==========================================

plt.figure(figsize=(9, 5))

launch_year_count.plot(kind="line", marker="o")

plt.title("Mutual Fund Schemes by Launch Year")
plt.xlabel("Launch Year")
plt.ylabel("Number of Schemes")

plt.tight_layout()

plt.savefig("data/charts/schemes_by_launch_year.png")

plt.close()


print("\n===== CHARTS CREATED SUCCESSFULLY =====")
print("1. schemes_by_category.png")
print("2. risk_category_distribution.png")
print("3. schemes_by_launch_year.png")
# ==========================================
# 14. SAVE CLEANED DATASET
# ==========================================

os.makedirs("data/processed", exist_ok=True)

df.to_csv(
    "data/processed/cleaned_fund_master.csv",
    index=False
)

print("\n===== CLEANED DATASET SAVED =====")
print("data/processed/cleaned_fund_master.csv")