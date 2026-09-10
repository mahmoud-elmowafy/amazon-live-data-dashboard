import sqlite3
import pandas as pd

# =========================
# File Paths
# =========================

csv_path = "data/amazon_search_clean.csv"
db_path = "data/amazon_analysis.db"


# =========================
# Load Clean CSV
# =========================

df = pd.read_csv(csv_path)


# =========================
# Connect to SQLite
# =========================

connection = sqlite3.connect(db_path)


# =========================
# Load Data into SQL Table
# =========================

df.to_sql(
    "amazon_products",
    connection,
    if_exists="replace",
    index=False
)


# =========================
# Verify Data
# =========================

query = """
SELECT *
FROM amazon_products
LIMIT 5;
"""

result = pd.read_sql_query(
    query,
    connection
)

print("=" * 60)
print("SQL DATABASE CREATED SUCCESSFULLY")
print("=" * 60)

print("\nFirst 5 rows:")
print(result.to_string(index=False))


# =========================
# Row Count
# =========================

count_query = """
SELECT COUNT(*) AS total_products
FROM amazon_products;
"""

count = pd.read_sql_query(
    count_query,
    connection
)

print()
print(f"Total products in SQL: {count['total_products'].iloc[0]}")


# =========================
# Close Connection
# =========================

connection.close()

print()
print(f"Database saved to: {db_path}")