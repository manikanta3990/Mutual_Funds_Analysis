from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text


# ============================================
# PATHS
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "bluestock_mf.db"
CHARTS_DIR = BASE_DIR / "charts"

CHARTS_DIR.mkdir(exist_ok=True)


# ============================================
# DATABASE CONNECTION
# ============================================

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

print("Database:", DB_PATH)
print("Charts folder:", CHARTS_DIR)


# ============================================
# HELPER FUNCTION
# ============================================

def save_chart(query, title, filename, chart_type="bar"):

    with engine.connect() as connection:

        df = pd.read_sql(
            text(query),
            connection
        )

    print("\nCreating:", title)

    plt.figure(figsize=(10, 6))

    if chart_type == "bar":

        plt.bar(
            df.iloc[:, 0],
            df.iloc[:, 1]
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

    elif chart_type == "pie":

        plt.pie(
            df.iloc[:, 1],
            labels=df.iloc[:, 0],
            autopct="%1.1f%%"
        )

    elif chart_type == "line":

        plt.plot(
            df.iloc[:, 0],
            df.iloc[:, 1],
            marker="o"
        )

        plt.xticks(
            rotation=45,
            ha="right"
        )

    plt.title(title)

    plt.tight_layout()

    output_path = CHARTS_DIR / filename

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved:", output_path)


# ============================================
# CHART 1
# TRANSACTIONS BY TYPE
# ============================================

query_1 = """
SELECT
    transaction_type,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_amount DESC;
"""

save_chart(
    query_1,
    "Total Transaction Amount by Transaction Type",
    "01_transaction_type_amount.png"
)


# ============================================
# CHART 2
# TRANSACTIONS BY AGE GROUP
# ============================================

query_2 = """
SELECT
    age_group,
    SUM(amount_inr) AS total_amount
FROM fact_transactions
GROUP BY age_group
ORDER BY total_amount DESC;
"""

save_chart(
    query_2,
    "Total Transaction Amount by Age Group",
    "02_transaction_amount_age_group.png"
)


# ============================================
# CHART 3
# AUM BY FUND HOUSE
# ============================================

query_3 = """
SELECT
    fund_house,
    SUM(aum_crore) AS total_aum
FROM fact_aum
GROUP BY fund_house
ORDER BY total_aum DESC
LIMIT 10;
"""

save_chart(
    query_3,
    "Top 10 Fund Houses by AUM",
    "03_top_fund_houses_aum.png"
)


# ============================================
# CHART 4
# TOP FUNDS BY SHARPE RATIO
# ============================================

query_4 = """
SELECT
    f.scheme_name,
    p.sharpe_ratio
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.sharpe_ratio DESC
LIMIT 10;
"""

save_chart(
    query_4,
    "Top 10 Mutual Funds by Sharpe Ratio",
    "04_top_sharpe_ratio.png"
)


# ============================================
# CHART 5
# TOP FUNDS BY AUM
# ============================================

query_5 = """
SELECT
    f.scheme_name,
    p.aum_crore
FROM fact_performance p
JOIN dim_fund f
    ON p.amfi_code = f.amfi_code
ORDER BY p.aum_crore DESC
LIMIT 10;
"""

save_chart(
    query_5,
    "Top 10 Mutual Funds by AUM",
    "05_top_funds_aum.png"
)


# ============================================
# COMPLETE
# ============================================

print("\n" + "=" * 60)
print("CHART CREATION COMPLETE")
print("=" * 60)

print("\nCharts saved in:")
print(CHARTS_DIR)