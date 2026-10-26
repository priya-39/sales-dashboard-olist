
import sqlite3
import pandas as pd

# Connect to the existing SQLite database
conn = sqlite3.connect("olist.db")

# Read and execute the saved SQL query
with open("sql/05_payment_mix.sql", "r", encoding="utf-8") as file:
    query = file.read()

df = pd.read_sql_query(query, conn)

# Export the results for Power BI
df.to_csv("data/processed/payment_mix.csv", index=False)

print("PAYMENT MIX RESULTS")
print(df.to_string(index=False))

print("\nTotal payment value (BRL):")
print(round(df["payment_value"].sum(), 2))

conn.close()
