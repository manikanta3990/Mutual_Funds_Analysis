from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

# ============================================
# PATHS
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"
SQL_DIR = BASE_DIR / "sql"

DB_PATH = BASE_DIR / "bluestock_mf.db"
SCHEMA_PATH = SQL_DIR / "schema.sql"


# ============================================
# DATABASE CONNECTION
# ============================================

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

print("Database:", DB_PATH)


# ============================================
# CREATE DATABASE TABLES
# ============================================

schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

raw_connection = engine.raw_connection()

try:
    raw_connection.executescript(schema_sql)
    raw_connection.commit()
finally:
    raw_connection.close()

print("Database schema created successfully!")

# ============================================
# LOAD CLEANED DATASETS
# ============================================

fund = pd.read_csv(
    PROCESSED_DIR / "cleaned_01_fund_master.csv"
)

nav = pd.read_csv(
    PROCESSED_DIR / "cleaned_02_nav_history.csv"
)

aum = pd.read_csv(
    PROCESSED_DIR / "cleaned_03_aum_by_fund_house.csv"
)

transactions = pd.read_csv(
    PROCESSED_DIR / "cleaned_08_investor_transactions.csv"
)

performance = pd.read_csv(
    PROCESSED_DIR / "cleaned_07_scheme_performance.csv"
)


print("\nCleaned datasets loaded into Pandas.")

print("Fund:", fund.shape)
print("NAV:", nav.shape)
print("AUM:", aum.shape)
print("Transactions:", transactions.shape)
print("Performance:", performance.shape)


# ============================================
# CREATE DATE DIMENSION
# ============================================

date_series = pd.concat(
    [
        pd.to_datetime(
            nav["date"],
            errors="coerce"
        ),

        pd.to_datetime(
            aum["date"],
            errors="coerce"
        ),

        pd.to_datetime(
            transactions["transaction_date"],
            errors="coerce"
        )
    ],
    ignore_index=True
)

date_series = (
    date_series
    .dropna()
    .drop_duplicates()
    .sort_values()
)

dim_date = pd.DataFrame({
    "full_date": date_series
})

dim_date["full_date"] = pd.to_datetime(
    dim_date["full_date"]
)

dim_date["date_key"] = (
    dim_date["full_date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

dim_date["year"] = (
    dim_date["full_date"].dt.year
)

dim_date["quarter"] = (
    dim_date["full_date"].dt.quarter
)

dim_date["month"] = (
    dim_date["full_date"].dt.month
)

dim_date["month_name"] = (
    dim_date["full_date"].dt.month_name()
)

dim_date["day"] = (
    dim_date["full_date"].dt.day
)

dim_date = dim_date[
    [
        "date_key",
        "full_date",
        "year",
        "quarter",
        "month",
        "month_name",
        "day"
    ]
]

print(
    "\nDate dimension rows:",
    len(dim_date)
)


# ============================================
# LOAD DIM FUND
# ============================================

fund.to_sql(
    "dim_fund",
    engine,
    if_exists="append",
    index=False,
    chunksize=500
)

print("dim_fund loaded!")


# ============================================
# LOAD DIM DATE
# ============================================

dim_date.to_sql(
    "dim_date",
    engine,
    if_exists="append",
    index=False,
    chunksize=500
)
print("dim_date loaded!")


# ============================================
# PREPARE FACT NAV
# ============================================

nav["date"] = pd.to_datetime(
    nav["date"]
)

date_lookup = dict(
    zip(
        dim_date["full_date"],
        dim_date["date_key"]
    )
)

nav["date_key"] = nav["date"].map(
    date_lookup
)

fact_nav = nav[
    [
        "amfi_code",
        "date_key",
        "nav"
    ]
].copy()


# ============================================
# LOAD FACT NAV
# ============================================

fact_nav.to_sql(
    "fact_nav",
    engine,
    if_exists="append",
    index=False,
    chunksize=500
)

print("fact_nav loaded!")


# ============================================
# LOAD FACT TRANSACTIONS
# ============================================

transactions.to_sql(
    "fact_transactions",
    engine,
    if_exists="append",
    index=False,
    chunksize=500
)

print("fact_transactions loaded!")


# ============================================
# LOAD FACT PERFORMANCE
# ============================================

performance.to_sql(
    "fact_performance",
    engine,
    if_exists="append",
    index=False,
    chunksize=500
)

print("fact_performance loaded!")


# ============================================
# LOAD FACT AUM
# ============================================

aum["date"] = pd.to_datetime(
    aum["date"]
)

aum["date_key"] = aum["date"].map(
    date_lookup
)

fact_aum = aum[
    [
        "date_key",
        "fund_house",
        "aum_lakh_crore",
        "aum_crore",
        "num_schemes"
    ]
].copy()

fact_aum.to_sql(
    "fact_aum",
    engine,
    if_exists="append",
    index=False,
    chunksize=500
)

print("fact_aum loaded!")


# ============================================
# VERIFY ROW COUNTS
# ============================================

print("\n================================")
print("DATABASE ROW COUNT VERIFICATION")
print("================================")

tables = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

with engine.connect() as connection:

    for table in tables:

        result = connection.execute(
            text(
                f"SELECT COUNT(*) FROM {table}"
            )
        )

        count = result.scalar()

        print(
            f"{table}: {count:,} rows"
        )


print("\n================================")
print("DATABASE CREATED SUCCESSFULLY!")
print("================================")

print(
    "SQLite database:",
    DB_PATH
)
print("\n================================")
print("TOTAL FUNDS")
print("================================")

with engine.connect() as connection:
    result = connection.execute(
        text("SELECT COUNT(*) FROM dim_fund")
    )

    total_funds = result.scalar()

    print("Total funds:", total_funds)