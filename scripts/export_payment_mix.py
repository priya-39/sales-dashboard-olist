from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "olist.db"
SQL_PATH = BASE_DIR / "sql" / "05_payment_mix.sql"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "payment_mix.csv"

query = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query(query, conn)

df.to_csv(OUTPUT_PATH, index=False)

print("PAYMENT MIX RESULTS")
print(df.to_string(index=False))
print("\nTotal payment value (BRL):")
print(round(df["payment_value"].sum(), 2))
