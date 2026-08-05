from pathlib import Path
import sqlite3

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite database
DB_PATH = BASE_DIR / "bluestock_mf.db"

# Connect to database
connection = sqlite3.connect(DB_PATH)
cursor = connection.cursor()

print("Database:", DB_PATH)

print("\n================================")
print("TABLES IN DATABASE")
print("================================")

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type = 'table'
ORDER BY name;
""")

tables = cursor.fetchall()

for table in tables:
    print(table[0])


print("\n================================")
print("ROW COUNT VERIFICATION")
print("================================")

table_names = [
    "dim_fund",
    "dim_date",
    "fact_nav",
    "fact_transactions",
    "fact_performance",
    "fact_aum"
]

for table in table_names:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table}: {count:,} rows")


print("\n================================")
print("SAMPLE DATA")
print("================================")

print("\nDIM_FUND:")
cursor.execute("""
SELECT *
FROM dim_fund
LIMIT 5;
""")

for row in cursor.fetchall():
    print(row)


print("\nDIM_DATE:")
cursor.execute("""
SELECT *
FROM dim_date
LIMIT 5;
""")

for row in cursor.fetchall():
    print(row)


print("\nFACT_NAV:")
cursor.execute("""
SELECT *
FROM fact_nav
LIMIT 5;
""")

for row in cursor.fetchall():
    print(row)


print("\nFACT_TRANSACTIONS:")
cursor.execute("""
SELECT *
FROM fact_transactions
LIMIT 5;
""")

for row in cursor.fetchall():
    print(row)


print("\nFACT_PERFORMANCE:")
cursor.execute("""
SELECT *
FROM fact_performance
LIMIT 5;
""")

for row in cursor.fetchall():
    print(row)


print("\nFACT_AUM:")
cursor.execute("""
SELECT *
FROM fact_aum
LIMIT 5;
""")

for row in cursor.fetchall():
    print(row)


# Close database
connection.close()

print("\n================================")
print("DATABASE VERIFICATION COMPLETE")
print("================================")