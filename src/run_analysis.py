from pathlib import Path
from sqlalchemy import create_engine, text

# ============================================
# PATHS
# ============================================

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "bluestock_mf.db"
SQL_FILE = BASE_DIR / "sql" / "analysis_queries.sql"

# ============================================
# DATABASE CONNECTION
# ============================================

engine = create_engine(
    f"sqlite:///{DB_PATH}"
)

print("Database:", DB_PATH)
print("SQL file:", SQL_FILE)

# ============================================
# READ SQL FILE
# ============================================

sql_text = SQL_FILE.read_text(
    encoding="utf-8"
)

# ============================================
# SPLIT QUERIES
# ============================================

queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

print("\nNumber of SQL queries:", len(queries))

# ============================================
# EXECUTE QUERIES
# ============================================

with engine.connect() as connection:

    for i, query in enumerate(queries, start=1):

        print("\n" + "=" * 70)
        print(f"QUERY {i}")
        print("=" * 70)

        print(query)

        try:

            result = connection.execute(
                text(query)
            )

            rows = result.fetchall()

            print("\nRESULT:")

            for row in rows:
                print(row)

        except Exception as error:

            print("\nERROR:")
            print(error)


print("\n" + "=" * 70)
print("SQL ANALYSIS COMPLETE")
print("=" * 70)