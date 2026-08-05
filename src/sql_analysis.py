from pathlib import Path
from sqlalchemy import create_engine, text
import pandas as pd

# ============================================
# PATH
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "bluestock_mf.db"

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

print("Database:", DB_PATH)


# ============================================
# FUNCTION TO RUN SQL
# ============================================

def run_query(title, query):

    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)

    with engine.connect() as connection:

        df = pd.read_sql(
            text(query),
            connection
        )

    print(df.to_string(index=False))

    return df


# ============================================
# QUERY 1 — TOTAL FUNDS
# ============================================

q1 = """
SELECT COUNT(*) AS total_funds
FROM dim_fund;
"""

run_query(
    "QUERY 1 — TOTAL FUNDS",
    q1
)


# ============================================
# QUERY 2 — FUNDS BY CATEGORY
# ============================================

q2 = """
SELECT
    category,
    COUNT(*) AS fund_count
FROM dim_fund
GROUP BY category
ORDER BY fund_count DESC;
"""

run_query(
    "QUERY 2 — FUNDS BY CATEGORY",
    q2
)


# ============================================
# QUERY 3 — FUNDS BY FUND HOUSE
# ============================================

q3 = """
SELECT
    fund_house,
    COUNT(*) AS fund_count
FROM dim_fund
GROUP BY fund_house
ORDER BY fund_count DESC;
"""

run_query(
    "QUERY 3 — FUNDS BY FUND HOUSE",
    q3
)


# ============================================
# QUERY 4 — AVERAGE EXPENSE RATIO
# ============================================

q4 = """
SELECT
    ROUND(AVG(expense_ratio_pct), 2)
        AS average_expense_ratio
FROM dim_fund;
"""

run_query(
    "QUERY 4 — AVERAGE EXPENSE RATIO",
    q4
)


# ============================================
# QUERY 5 — TRANSACTION TYPES
# ============================================

q5 = """
SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;
"""

run_query(
    "QUERY 5 — TRANSACTION TYPES",
    q5
)


# ============================================
# QUERY 6 — TRANSACTIONS BY AGE GROUP
# ============================================

q6 = """
SELECT
    age_group,
    COUNT(*) AS transaction_count,
    ROUND(SUM(amount_inr), 2) AS total_amount
FROM fact_transactions
GROUP BY age_group
ORDER BY total_amount DESC;
"""

run_query(
    "QUERY 6 — TRANSACTIONS BY AGE GROUP",
    q6
)


# ============================================
# QUERY 7 — AUM BY FUND HOUSE
# ============================================

q7 = """
SELECT
    fund_house,
    ROUND(SUM(aum_crore), 2) AS total_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum_crore DESC;
"""

run_query(
    "QUERY 7 — AUM BY FUND HOUSE",
    q7
)


# ============================================
# QUERY 8 — TOP FUNDS BY SHARPE RATIO
# ============================================

q8 = """
SELECT
    f.scheme_name,
    p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 10;
"""

run_query(
    "QUERY 8 — TOP FUNDS BY SHARPE RATIO",
    q8
)


# ============================================
# QUERY 9 — TOP FUNDS BY AUM
# ============================================

q9 = """
SELECT
    f.scheme_name,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 10;
"""

run_query(
    "QUERY 9 — TOP FUNDS BY AUM",
    q9
)


# ============================================
# QUERY 10 — NAV RECORDS BY FUND
# ============================================

q10 = """
SELECT
    amfi_code,
    COUNT(*) AS nav_records
FROM fact_nav
GROUP BY amfi_code
ORDER BY nav_records DESC;
"""

run_query(
    "QUERY 10 — NAV RECORDS BY FUND",
    q10
)


# ============================================
# COMPLETE
# ============================================

print("\n" + "=" * 70)
print("SQL ANALYSIS COMPLETE")
print("=" * 70)