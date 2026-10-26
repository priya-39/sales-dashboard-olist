
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "olist.db"
SQL_PATH = BASE_DIR / "sql" / "sales_analysis.sql"

sql_text = SQL_PATH.read_text(encoding="utf-8")

with sqlite3.connect(DB_PATH) as conn:
    queries = [
        query.strip()
        for query in sql_text.split(";")
        if query.strip()
    ]

    for i, query in enumerate(queries, start=1):
        print(f"\n{'=' * 50}")
        print(f"QUERY {i}")

        result = pd.read_sql_query(query, conn)
        print(result.to_string(index=False))
