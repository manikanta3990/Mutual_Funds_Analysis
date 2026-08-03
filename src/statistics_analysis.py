import pandas as pd
import numpy as np

# Load cleaned dataset
df = pd.read_csv("data/processed/cleaned_fund_master.csv")

print("===== DATASET =====")
print(df.head())

print("\n===== BASIC INFORMATION =====")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


# ==========================================
# 1. MEAN
# ==========================================

print("\n===== MEAN =====")

print("Average Expense Ratio:",
      df["expense_ratio_pct"].mean())

print("Average Exit Load:",
      df["exit_load_pct"].mean())


# ==========================================
# 2. MEDIAN
# ==========================================

print("\n===== MEDIAN =====")

print("Median Expense Ratio:",
      df["expense_ratio_pct"].median())

print("Median Exit Load:",
      df["exit_load_pct"].median())


# ==========================================
# 3. MODE
# ==========================================

print("\n===== MODE =====")

print("Mode Expense Ratio:")
print(df["expense_ratio_pct"].mode())

print("Mode Exit Load:")
print(df["exit_load_pct"].mode())


# ==========================================
# 4. STANDARD DEVIATION
# ==========================================

print("\n===== STANDARD DEVIATION =====")

print("Expense Ratio Standard Deviation:",
      df["expense_ratio_pct"].std())

print("Exit Load Standard Deviation:",
      df["exit_load_pct"].std())


# ==========================================
# 5. CORRELATION
# ==========================================

print("\n===== CORRELATION =====")

correlation = df[
    ["expense_ratio_pct", "exit_load_pct"]
].corr()

print(correlation)


# ==========================================
# 6. PROBABILITY
# ==========================================

print("\n===== PROBABILITY =====")

total_schemes = len(df)

high_expense_schemes = len(
    df[df["expense_ratio_pct"] > df["expense_ratio_pct"].mean()]
)

probability = high_expense_schemes / total_schemes

print(
    "Probability of selecting a scheme "
    "with above-average expense ratio:",
    probability
)


# ==========================================
# 7. SIMPLE REGRESSION
# ==========================================

print("\n===== REGRESSION =====")

x = df["expense_ratio_pct"]
y = df["exit_load_pct"]

slope, intercept = np.polyfit(x, y, 1)

print("Slope:", slope)
print("Intercept:", intercept)

print(
    "Regression Equation:"
    f" Exit Load = {slope:.4f} * Expense Ratio + {intercept:.4f}"
)


print("\n===== STATISTICS ANALYSIS COMPLETED =====")