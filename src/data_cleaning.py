import pandas as pd
from pathlib import Path

# ---------------------------------------
# 1. File paths
# ---------------------------------------
input_file = Path("data/raw/02_nav_history.csv")
output_file = Path("data/processed/cleaned_02_nav_history.csv")

# Create processed folder if it doesn't exist
output_file.parent.mkdir(parents=True, exist_ok=True)

# ---------------------------------------
# 2. Load data
# ---------------------------------------
df = pd.read_csv(input_file)

print("Original shape:", df.shape)
print("\nOriginal columns:")
print(df.columns.tolist())

# ---------------------------------------
# 3. Parse date
# ---------------------------------------
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Check invalid dates
invalid_dates = df["date"].isna().sum()
print("\nInvalid dates:", invalid_dates)

# Remove rows where date could not be parsed
df = df.dropna(subset=["date"])

# ---------------------------------------
# 4. Convert NAV to numeric
# ---------------------------------------
df["nav"] = pd.to_numeric(df["nav"], errors="coerce")

invalid_nav = df["nav"].isna().sum()
print("Invalid NAV values:", invalid_nav)

# Remove rows with invalid NAV
df = df.dropna(subset=["nav"])

# ---------------------------------------
# 5. Sort by AMFI code and date
# ---------------------------------------
df = df.sort_values(
    by=["amfi_code", "date"]
).reset_index(drop=True)

# ---------------------------------------
# 6. Remove duplicates
# ---------------------------------------
duplicates_before = df.duplicated(
    subset=["amfi_code", "date"]
).sum()

print("Duplicate rows found:", duplicates_before)

df = df.drop_duplicates(
    subset=["amfi_code", "date"],
    keep="last"
).reset_index(drop=True)

# ---------------------------------------
# 7. Forward-fill NAV within each fund
# ---------------------------------------
df["nav"] = df.groupby("amfi_code")["nav"].ffill()

# ---------------------------------------
# 8. Validate NAV > 0
# ---------------------------------------
invalid_positive_nav = (df["nav"] <= 0).sum()

print("NAV values <= 0:", invalid_positive_nav)

# Remove invalid NAV values
df = df[df["nav"] > 0].reset_index(drop=True)

# ---------------------------------------
# 9. Save cleaned dataset
# ---------------------------------------
df.to_csv(output_file, index=False)

# ---------------------------------------
# 10. Final summary
# ---------------------------------------
print("\nCleaning completed successfully!")
print("Final shape:", df.shape)
print("Output file:", output_file)

print("\nRemaining missing values:")
print(df.isnull().sum())
# ==========================================
# CLEAN INVESTOR TRANSACTIONS
# ==========================================

transactions_input = Path("data/raw/08_investor_transactions.csv")
transactions_output = Path(
    "data/processed/cleaned_08_investor_transactions.csv"
)

transactions = pd.read_csv(transactions_input)

print("\n--- Investor Transactions Cleaning ---")
print("Original shape:", transactions.shape)

# 1. Parse transaction date
transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

invalid_dates = transactions["transaction_date"].isna().sum()
print("Invalid dates:", invalid_dates)

transactions = transactions.dropna(
    subset=["transaction_date"]
)

# 2. Standardize transaction types
transactions["transaction_type"] = (
    transactions["transaction_type"]
    .astype(str)
    .str.strip()
)

# Convert case-insensitively
transaction_mapping = {
    "sip": "SIP",
    "lumpsum": "Lumpsum",
    "redemption": "Redemption"
}

transactions["transaction_type"] = (
    transactions["transaction_type"]
    .str.lower()
    .map(transaction_mapping)
)

invalid_transaction_types = (
    transactions["transaction_type"].isna()
).sum()

print(
    "Invalid transaction types:",
    invalid_transaction_types
)

transactions = transactions.dropna(
    subset=["transaction_type"]
)

# 3. Convert amount to numeric
transactions["amount_inr"] = pd.to_numeric(
    transactions["amount_inr"],
    errors="coerce"
)

invalid_amounts = (
    transactions["amount_inr"].isna()
).sum()

print("Invalid numeric amounts:", invalid_amounts)

transactions = transactions.dropna(
    subset=["amount_inr"]
)

# 4. Validate amount > 0
amounts_less_equal_zero = (
    transactions["amount_inr"] <= 0
).sum()

print(
    "Amount <= 0:",
    amounts_less_equal_zero
)

transactions = transactions[
    transactions["amount_inr"] > 0
]

# 5. Standardize KYC status
transactions["kyc_status"] = (
    transactions["kyc_status"]
    .astype(str)
    .str.strip()
)

kyc_mapping = {
    "verified": "Verified",
    "pending": "Pending"
}

transactions["kyc_status"] = (
    transactions["kyc_status"]
    .str.lower()
    .map(kyc_mapping)
)

invalid_kyc = (
    transactions["kyc_status"].isna()
).sum()

print("Invalid KYC statuses:", invalid_kyc)

transactions = transactions.dropna(
    subset=["kyc_status"]
)

# 6. Remove exact duplicate rows
duplicates = transactions.duplicated().sum()

print("Duplicate rows:", duplicates)

transactions = transactions.drop_duplicates()

# 7. Sort
transactions = transactions.sort_values(
    by=["transaction_date", "investor_id"]
).reset_index(drop=True)

# 8. Save
transactions.to_csv(
    transactions_output,
    index=False
)

print("Final shape:", transactions.shape)

print(
    "Saved to:",
    transactions_output
)

print("\nFinal transaction types:")
print(
    transactions["transaction_type"]
    .value_counts()
)

print("\nFinal KYC values:")
print(
    transactions["kyc_status"]
    .value_counts()
)

print("\nRemaining missing values:")
print(transactions.isnull().sum())
# ==========================================
# CLEAN SCHEME PERFORMANCE
# ==========================================

performance_input = Path("data/raw/07_scheme_performance.csv")
performance_output = Path(
    "data/processed/cleaned_07_scheme_performance.csv"
)

performance = pd.read_csv(performance_input)

print("\n--- Scheme Performance Cleaning ---")
print("Original shape:", performance.shape)

# 1. Return columns that must be numeric
return_columns = [
    "return_1yr_pct",
    "return_3yr_pct",
    "return_5yr_pct",
    "benchmark_3yr_pct"
]

for column in return_columns:
    performance[column] = pd.to_numeric(
        performance[column],
        errors="coerce"
    )

# Count invalid return values
invalid_returns = performance[return_columns].isna().sum().sum()

print("Invalid return values:", invalid_returns)

# Remove rows with invalid returns
performance = performance.dropna(
    subset=return_columns
)

# 2. Expense ratio validation
performance["expense_ratio_pct"] = pd.to_numeric(
    performance["expense_ratio_pct"],
    errors="coerce"
)

invalid_expense = (
    performance["expense_ratio_pct"].isna()
).sum()

print("Invalid expense ratio values:", invalid_expense)

# Remove missing expense ratio
performance = performance.dropna(
    subset=["expense_ratio_pct"]
)

# Check expense ratio range
outside_expense_range = (
    (performance["expense_ratio_pct"] < 0.1) |
    (performance["expense_ratio_pct"] > 2.5)
).sum()

print(
    "Expense ratios outside 0.1%-2.5%:",
    outside_expense_range
)

# Flag anomalies instead of deleting valid records
performance["expense_ratio_anomaly"] = (
    (performance["expense_ratio_pct"] < 0.1) |
    (performance["expense_ratio_pct"] > 2.5)
)

# 3. Check duplicate rows
duplicates = performance.duplicated().sum()

print("Duplicate rows:", duplicates)

performance = performance.drop_duplicates()

# 4. Save cleaned data
performance.to_csv(
    performance_output,
    index=False
)

print("Final shape:", performance.shape)

print(
    "Saved to:",
    performance_output
)

print("\nExpense ratio anomaly count:")
print(
    performance["expense_ratio_anomaly"].value_counts()
)

print("\nRemaining missing values:")
print(performance.isnull().sum())
# ==========================================
# CLEAN FUND MASTER
# ==========================================

fund_input = Path("data/raw/01_fund_master.csv")
fund_output = Path(
    "data/processed/cleaned_01_fund_master.csv"
)

fund = pd.read_csv(fund_input)

print("\n--- Fund Master Cleaning ---")
print("Original shape:", fund.shape)

# 1. Parse launch date
fund["launch_date"] = pd.to_datetime(
    fund["launch_date"],
    errors="coerce"
)

print(
    "Invalid launch dates:",
    fund["launch_date"].isna().sum()
)

fund = fund.dropna(
    subset=["launch_date"]
)

# 2. Validate AMFI code
fund["amfi_code"] = pd.to_numeric(
    fund["amfi_code"],
    errors="coerce"
)

print(
    "Invalid AMFI codes:",
    fund["amfi_code"].isna().sum()
)

fund = fund.dropna(
    subset=["amfi_code"]
)

# 3. Validate expense ratio
fund["expense_ratio_pct"] = pd.to_numeric(
    fund["expense_ratio_pct"],
    errors="coerce"
)

print(
    "Invalid expense ratios:",
    fund["expense_ratio_pct"].isna().sum()
)

# 4. Validate SIP and lumpsum amounts
for column in ["min_sip_amount", "min_lumpsum_amount"]:
    fund[column] = pd.to_numeric(
        fund[column],
        errors="coerce"
    )

print(
    "Invalid SIP amounts:",
    fund["min_sip_amount"].isna().sum()
)

print(
    "Invalid lumpsum amounts:",
    fund["min_lumpsum_amount"].isna().sum()
)

# 5. Remove exact duplicate rows
duplicates = fund.duplicated().sum()

print("Duplicate rows:", duplicates)

fund = fund.drop_duplicates()

# 6. Standardize text columns
text_columns = [
    "fund_house",
    "scheme_name",
    "category",
    "sub_category",
    "plan",
    "benchmark",
    "fund_manager",
    "risk_category",
    "sebi_category_code"
]

for column in text_columns:
    fund[column] = (
        fund[column]
        .astype(str)
        .str.strip()
    )

# 7. Sort by AMFI code
fund = fund.sort_values(
    by="amfi_code"
).reset_index(drop=True)

# 8. Save cleaned dataset
fund.to_csv(
    fund_output,
    index=False
)

print("Final shape:", fund.shape)
print("Saved to:", fund_output)

print("\nRemaining missing values:")
print(fund.isnull().sum())
# ==========================================
# CLEAN AUM BY FUND HOUSE
# ==========================================

aum_input = Path("data/raw/03_aum_by_fund_house.csv")
aum_output = Path(
    "data/processed/cleaned_03_aum_by_fund_house.csv"
)

aum = pd.read_csv(aum_input)

print("\n--- AUM by Fund House Cleaning ---")
print("Original shape:", aum.shape)

# 1. Parse date
aum["date"] = pd.to_datetime(
    aum["date"],
    errors="coerce"
)

print(
    "Invalid dates:",
    aum["date"].isna().sum()
)

aum = aum.dropna(
    subset=["date"]
)

# 2. Convert numeric columns
numeric_columns = [
    "aum_lakh_crore",
    "aum_crore",
    "num_schemes"
]

for column in numeric_columns:
    aum[column] = pd.to_numeric(
        aum[column],
        errors="coerce"
    )

# Check invalid numeric values
print(
    "Invalid numeric values:",
    aum[numeric_columns].isna().sum().sum()
)

aum = aum.dropna(
    subset=numeric_columns
)

# 3. Validate AUM values > 0
invalid_aum = (
    (aum["aum_lakh_crore"] <= 0) |
    (aum["aum_crore"] <= 0)
).sum()

print("Invalid AUM values <= 0:", invalid_aum)

aum = aum[
    (aum["aum_lakh_crore"] > 0) &
    (aum["aum_crore"] > 0)
]

# 4. Validate number of schemes
invalid_schemes = (
    aum["num_schemes"] <= 0
).sum()

print(
    "Invalid number of schemes:",
    invalid_schemes
)

aum = aum[
    aum["num_schemes"] > 0
]

# 5. Standardize fund house names
aum["fund_house"] = (
    aum["fund_house"]
    .astype(str)
    .str.strip()
)

# 6. Remove duplicates
duplicates = aum.duplicated().sum()

print("Duplicate rows:", duplicates)

aum = aum.drop_duplicates()

# 7. Sort
aum = aum.sort_values(
    by=["date", "fund_house"]
).reset_index(drop=True)

# 8. Save
aum.to_csv(
    aum_output,
    index=False
)

print("Final shape:", aum.shape)
print("Saved to:", aum_output)

print("\nRemaining missing values:")
print(aum.isnull().sum())
# ==========================================
# CLEAN MONTHLY SIP INFLOWS
# ==========================================

sip_input = Path("data/raw/04_monthly_sip_inflows.csv")
sip_output = Path(
    "data/processed/cleaned_04_monthly_sip_inflows.csv"
)

sip = pd.read_csv(sip_input)

print("\n--- Monthly SIP Inflows Cleaning ---")
print("Original shape:", sip.shape)

# 1. Parse month
sip["month"] = pd.to_datetime(
    sip["month"],
    errors="coerce"
)

print(
    "Invalid months:",
    sip["month"].isna().sum()
)

sip = sip.dropna(
    subset=["month"]
)

# 2. Convert numeric columns
numeric_columns = [
    "sip_inflow_crore",
    "active_sip_accounts_crore",
    "new_sip_accounts_lakh",
    "sip_aum_lakh_crore",
    "yoy_growth_pct"
]

for column in numeric_columns:
    sip[column] = pd.to_numeric(
        sip[column],
        errors="coerce"
    )

print(
    "Invalid numeric values:",
    sip[numeric_columns].isna().sum().sum()
)

# 3. Validate positive SIP metrics
positive_columns = [
    "sip_inflow_crore",
    "active_sip_accounts_crore",
    "new_sip_accounts_lakh",
    "sip_aum_lakh_crore"
]

for column in positive_columns:
    invalid_count = (
        sip[column] <= 0
    ).sum()

    print(
        f"Invalid {column} <= 0:",
        invalid_count
    )

    sip = sip[
        sip[column] > 0
    ]

# 4. YoY growth
# First 12 months may legitimately be missing
print(
    "Missing YoY growth values:",
    sip["yoy_growth_pct"].isna().sum()
)

# 5. Remove duplicate rows
duplicates = sip.duplicated().sum()

print("Duplicate rows:", duplicates)

sip = sip.drop_duplicates()

# 6. Sort by month
sip = sip.sort_values(
    by="month"
).reset_index(drop=True)

# 7. Save
sip.to_csv(
    sip_output,
    index=False
)

print("Final shape:", sip.shape)
print("Saved to:", sip_output)

print("\nRemaining missing values:")
print(sip.isnull().sum())
# ==========================================
# CLEAN CATEGORY INFLOWS
# ==========================================

category_input = Path("data/raw/05_category_inflows.csv")
category_output = Path(
    "data/processed/cleaned_05_category_inflows.csv"
)

category = pd.read_csv(category_input)

print("\n--- Category Inflows Cleaning ---")
print("Original shape:", category.shape)

# 1. Parse month
category["month"] = pd.to_datetime(
    category["month"],
    errors="coerce"
)

print(
    "Invalid months:",
    category["month"].isna().sum()
)

category = category.dropna(
    subset=["month"]
)

# 2. Standardize category names
category["category"] = (
    category["category"]
    .astype(str)
    .str.strip()
)

# 3. Convert net inflow to numeric
category["net_inflow_crore"] = pd.to_numeric(
    category["net_inflow_crore"],
    errors="coerce"
)

print(
    "Invalid net inflow values:",
    category["net_inflow_crore"].isna().sum()
)

category = category.dropna(
    subset=["net_inflow_crore"]
)

# 4. Check duplicate rows
duplicates = category.duplicated().sum()

print("Duplicate rows:", duplicates)

category = category.drop_duplicates()

# 5. Check category values
print("\nNumber of unique categories:")
print(category["category"].nunique())

# 6. Sort
category = category.sort_values(
    by=["month", "category"]
).reset_index(drop=True)

# 7. Save
category.to_csv(
    category_output,
    index=False
)

print("Final shape:", category.shape)
print("Saved to:", category_output)

print("\nRemaining missing values:")
print(category.isnull().sum())
# ==========================================
# CLEAN INDUSTRY FOLIO COUNT
# ==========================================

folio_input = Path("data/raw/06_industry_folio_count.csv")
folio_output = Path(
    "data/processed/cleaned_06_industry_folio_count.csv"
)

folio = pd.read_csv(folio_input)

print("\n--- Industry Folio Count Cleaning ---")
print("Original shape:", folio.shape)

# 1. Parse month
folio["month"] = pd.to_datetime(
    folio["month"],
    errors="coerce"
)

print(
    "Invalid months:",
    folio["month"].isna().sum()
)

folio = folio.dropna(
    subset=["month"]
)

# 2. Convert numeric columns
numeric_columns = [
    "total_folios_crore",
    "equity_folios_crore",
    "debt_folios_crore",
    "hybrid_folios_crore",
    "others_folios_crore"
]

for column in numeric_columns:
    folio[column] = pd.to_numeric(
        folio[column],
        errors="coerce"
    )

print(
    "Invalid numeric values:",
    folio[numeric_columns].isna().sum().sum()
)

folio = folio.dropna(
    subset=numeric_columns
)

# 3. Validate values are positive
for column in numeric_columns:
    invalid_count = (
        folio[column] <= 0
    ).sum()

    print(
        f"Invalid {column} <= 0:",
        invalid_count
    )

    folio = folio[
        folio[column] > 0
    ]

# 4. Remove duplicates
duplicates = folio.duplicated().sum()

print("Duplicate rows:", duplicates)

folio = folio.drop_duplicates()

# 5. Sort by month
folio = folio.sort_values(
    by="month"
).reset_index(drop=True)

# 6. Save cleaned file
folio.to_csv(
    folio_output,
    index=False
)

print("Final shape:", folio.shape)
print("Saved to:", folio_output)

print("\nRemaining missing values:")
print(folio.isnull().sum())
# ==========================================
# CLEAN PORTFOLIO HOLDINGS
# ==========================================

portfolio_input = Path(
    "data/raw/09_portfolio_holdings.csv"
)

portfolio_output = Path(
    "data/processed/cleaned_09_portfolio_holdings.csv"
)

portfolio = pd.read_csv(portfolio_input)

print("\n--- Portfolio Holdings Cleaning ---")
print("Original shape:", portfolio.shape)

# 1. Convert AMFI code to numeric
portfolio["amfi_code"] = pd.to_numeric(
    portfolio["amfi_code"],
    errors="coerce"
)

print(
    "Invalid AMFI codes:",
    portfolio["amfi_code"].isna().sum()
)

portfolio = portfolio.dropna(
    subset=["amfi_code"]
)

portfolio["amfi_code"] = (
    portfolio["amfi_code"].astype(int)
)

# 2. Convert portfolio date
portfolio["portfolio_date"] = pd.to_datetime(
    portfolio["portfolio_date"],
    errors="coerce"
)

print(
    "Invalid portfolio dates:",
    portfolio["portfolio_date"].isna().sum()
)

portfolio = portfolio.dropna(
    subset=["portfolio_date"]
)

# 3. Convert numeric columns
numeric_columns = [
    "weight_pct",
    "market_value_cr",
    "current_price_inr"
]

for column in numeric_columns:
    portfolio[column] = pd.to_numeric(
        portfolio[column],
        errors="coerce"
    )

print(
    "Invalid numeric values:",
    portfolio[numeric_columns].isna().sum().sum()
)

portfolio = portfolio.dropna(
    subset=numeric_columns
)

# 4. Clean text columns
text_columns = [
    "stock_symbol",
    "stock_name",
    "sector"
]

for column in text_columns:
    portfolio[column] = (
        portfolio[column]
        .astype(str)
        .str.strip()
    )

# 5. Validate weight
invalid_weight = (
    (portfolio["weight_pct"] <= 0) |
    (portfolio["weight_pct"] > 100)
).sum()

print(
    "Invalid weight percentages:",
    invalid_weight
)

portfolio = portfolio[
    (portfolio["weight_pct"] > 0) &
    (portfolio["weight_pct"] <= 100)
]

# 6. Validate market value
invalid_market_value = (
    portfolio["market_value_cr"] <= 0
).sum()

print(
    "Invalid market values <= 0:",
    invalid_market_value
)

portfolio = portfolio[
    portfolio["market_value_cr"] > 0
]

# 7. Validate current price
invalid_price = (
    portfolio["current_price_inr"] <= 0
).sum()

print(
    "Invalid current prices <= 0:",
    invalid_price
)

portfolio = portfolio[
    portfolio["current_price_inr"] > 0
]

# 8. Remove duplicates
duplicates = portfolio.duplicated().sum()

print(
    "Duplicate rows:",
    duplicates
)

portfolio = portfolio.drop_duplicates()

# 9. Sort
portfolio = portfolio.sort_values(
    by=["amfi_code", "portfolio_date", "weight_pct"],
    ascending=[True, True, False]
).reset_index(drop=True)

# 10. Save
portfolio.to_csv(
    portfolio_output,
    index=False
)

print(
    "Final shape:",
    portfolio.shape
)

print(
    "Saved to:",
    portfolio_output
)

print("\nRemaining missing values:")
print(portfolio.isnull().sum())
# ==========================================
# CLEAN BENCHMARK INDICES
# ==========================================

benchmark_input = Path(
    "data/raw/10_benchmark_indices.csv"
)

benchmark_output = Path(
    "data/processed/cleaned_10_benchmark_indices.csv"
)

benchmark = pd.read_csv(benchmark_input)

print("\n--- Benchmark Indices Cleaning ---")
print("Original shape:", benchmark.shape)

# 1. Convert date
benchmark["date"] = pd.to_datetime(
    benchmark["date"],
    errors="coerce"
)

print(
    "Invalid dates:",
    benchmark["date"].isna().sum()
)

benchmark = benchmark.dropna(
    subset=["date"]
)

# 2. Clean index names
benchmark["index_name"] = (
    benchmark["index_name"]
    .astype(str)
    .str.strip()
)

print(
    "Missing index names:",
    benchmark["index_name"].isna().sum()
)

# 3. Convert close value to numeric
benchmark["close_value"] = pd.to_numeric(
    benchmark["close_value"],
    errors="coerce"
)

print(
    "Invalid close values:",
    benchmark["close_value"].isna().sum()
)

benchmark = benchmark.dropna(
    subset=["close_value"]
)

# 4. Validate close value > 0
invalid_close = (
    benchmark["close_value"] <= 0
).sum()

print(
    "Close values <= 0:",
    invalid_close
)

benchmark = benchmark[
    benchmark["close_value"] > 0
]

# 5. Remove duplicates
duplicates = benchmark.duplicated().sum()

print(
    "Duplicate rows:",
    duplicates
)

benchmark = benchmark.drop_duplicates()

# 6. Sort by index and date
benchmark = benchmark.sort_values(
    by=["index_name", "date"]
).reset_index(drop=True)

# 7. Save cleaned dataset
benchmark.to_csv(
    benchmark_output,
    index=False
)

print(
    "Final shape:",
    benchmark.shape
)

print(
    "Saved to:",
    benchmark_output
)

print("\nRemaining missing values:")
print(benchmark.isnull().sum())