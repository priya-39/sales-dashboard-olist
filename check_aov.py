
import sqlite3

conn = sqlite3.connect("olist.db")
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

# Query 2: Delivered orders and payment value
cursor.execute("""
SELECT COUNT(*) AS delivered_orders,
       ROUND(SUM(p.order_payment), 2) AS delivered_payment
FROM olist_orders_dataset o
JOIN (
    SELECT order_id, SUM(payment_value) AS order_payment
    FROM olist_order_payments_dataset
    GROUP BY order_id
) p ON p.order_id = o.order_id
WHERE o.order_status = 'delivered';
""")

print("\nDELIVERED ORDERS AND PAYMENT")
print(cursor.fetchone())


import csv

delivered_orders = 96477
delivered_payment = 15422461.77
aov = delivered_payment / delivered_orders

with open("data/processed/aov_summary.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "delivered_orders_with_payment",
        "delivered_payment_brl",
        "aov_brl"
    ])
    writer.writerow([
        delivered_orders,
        round(delivered_payment, 2),
        round(aov, 2)
    ])

print("\nAOV SUMMARY CSV CREATED")
print("Delivered orders with payment:", delivered_orders)
print("Delivered payment (BRL):", round(delivered_payment, 2))
print("AOV (BRL):", round(aov, 2))

conn.close()
