from pathlib import Path
import sqlite3
import pandas as pd

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "raw"
DB_PATH = BASE_DIR / "olist.db"

# Find CSV files
csv_files = sorted(DATA_DIR.glob("*.csv"))

if not csv_files:
    raise FileNotFoundError(
        f"No CSV files found in {DATA_DIR}"
    )

# Load each CSV into SQLite
with sqlite3.connect(DB_PATH) as conn:
    for file in csv_files:
        table_name = file.stem

        print(f"Loading: {file.name}")

        df = pd.read_csv(file)
        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"  Rows loaded: {len(df):,}")

    # Verify tables
    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """,
        conn
    )

print("\nDatabase created:", DB_PATH.name)
print("Tables created:", len(tables))
print(tables.to_string(index=False))
