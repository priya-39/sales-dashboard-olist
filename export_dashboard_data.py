
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "olist.db"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

queries = {
    "monthly_orders": """
        SELECT
            strftime('%Y-%m', order_purchase_timestamp) AS month,
            COUNT(*) AS total_orders
        FROM olist_orders_dataset
        WHERE order_purchase_timestamp IS NOT NULL
        GROUP BY month
        ORDER BY month
    """,

    "monthly_payments": """
        SELECT
            strftime('%Y-%m', o.order_purchase_timestamp) AS month,
            ROUND(SUM(p.payment_value), 2) AS payment_value
        FROM olist_orders_dataset o
        JOIN olist_order_payments_dataset p
            ON o.order_id = p.order_id
        WHERE o.order_status = 'delivered'
          AND o.order_purchase_timestamp IS NOT NULL
        GROUP BY month
        ORDER BY month
    """,

    "category_sales": """
        SELECT
            COALESCE(
                t.product_category_name_english,
                p.product_category_name,
                'unknown'
            ) AS category,
            ROUND(SUM(oi.price), 2) AS item_sales_value
        FROM olist_order_items_dataset oi
        JOIN olist_products_dataset p
            ON oi.product_id = p.product_id
        LEFT JOIN product_category_name_translation t
            ON p.product_category_name = t.product_category_name
        GROUP BY category
        ORDER BY item_sales_value DESC
    """
}

with sqlite3.connect(DB_PATH) as conn:
    for name, query in queries.items():
        df = pd.read_sql_query(query, conn)
        output_path = OUTPUT_DIR / f"{name}.csv"
        df.to_csv(output_path, index=False)
        print(f"Saved {output_path.name}: {len(df)} rows")

print("Dashboard data export complete.")
