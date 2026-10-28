"""Check delivered orders, delivered payment value and AOV, then write aov_summary.csv."""

import csv
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "olist.db"
OUTPUT_PATH = BASE_DIR / "data" / "processed" / "aov_summary.csv"

with sqlite3.connect(DB_PATH) as conn:
    cursor = conn.cursor()

    # Query 1: Count orders by status
    cursor.execute("""
        SELECT order_status, COUNT(*) AS orders
        FROM olist_orders_dataset
        GROUP BY order_status
        ORDER BY orders DESC;
    """)
    print("ORDERS BY STATUS")
    for row in cursor.fetchall():
        print(row)

    # Query 2: Delivered orders with a payment record, and their payment value
    cursor.execute("""
        SELECT COUNT(*) AS delivered_orders_with_payment,
               ROUND(SUM(p.order_payment), 2) AS delivered_payment
        FROM olist_orders_dataset o
        JOIN (
            SELECT order_id, SUM(payment_value) AS order_payment
            FROM olist_order_payments_dataset
            GROUP BY order_id
        ) p ON p.order_id = o.order_id
        WHERE o.order_status = 'delivered';
    """)
    delivered_orders, delivered_payment = cursor.fetchone()

aov = delivered_payment / delivered_orders

print("\nDELIVERED ORDERS AND PAYMENT")
print("Delivered orders with payment:", delivered_orders)
print("Delivered payment (BRL):", delivered_payment)
print("AOV (BRL):", round(aov, 2))

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_PATH, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["delivered_orders_with_payment", "delivered_payment_brl", "aov_brl"])
    writer.writerow([delivered_orders, round(delivered_payment, 2), round(aov, 2)])

print("\nAOV SUMMARY CSV CREATED:", OUTPUT_PATH.name)
