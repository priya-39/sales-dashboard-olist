# Data Quality Checks

All checks were run on the Olist Brazilian e-commerce dataset after loading it into SQLite (`scripts/load_data.py`, `scripts/load_to_sqlite.py`, `scripts/run_sql.py`, `scripts/check_aov.py`).

## 1. Row Counts, Duplicates and Missing Values

| Table | Rows | Fully Duplicate Rows | Missing Values |
|---|---:|---:|---|
| customers | 99,441 | 0 | None |
| orders | 99,441 | 0 | order_approved_at: 160; order_delivered_carrier_date: 1,783; order_delivered_customer_date: 2,965 |
| order_items | 112,650 | 0 | None |
| order_payments | 103,886 | 0 | None |
| order_reviews | 99,224 | 0 | review_comment_title: 87,656; review_comment_message: 58,247 |
| products | 32,951 | 0 | Category and 3 other text/photo columns: 610 each; 4 size/weight columns: 2 each |
| sellers | 3,095 | 0 | None |
| product_category_name_translation | 71 | 0 | None |

Note: Duplicate rows means completely identical rows. Duplicates by order_id were not tested separately.

## 2. Order Status

| Status | Orders |
|---|---:|
| delivered | 96,478 |
| shipped | 1,107 |
| canceled | 625 |
| unavailable | 609 |
| invoiced | 314 |
| processing | 301 |
| created | 5 |
| approved | 2 |
| **Total** | **99,441** |

Delivered rate: 96,478 / 99,441 = 97.02%.

## 3. Payments

- The order_payments table has 103,886 rows for 99,441 orders. Some orders have multiple payment rows, for example installments or vouchers. Order counts should use COUNT(DISTINCT order_id).
- One delivered order has no payment record. Delivered orders with a payment record: 96,477 out of 96,478.
- Average order value (AOV) uses these 96,477 orders.
- An order can use more than one payment type, so order counts per payment type can add up to more than the number of orders.

## 4. Incomplete Months

| Month | Orders (All Statuses) |
|---|---:|
| 2016-09 | 4 |
| 2016-10 | 324 |
| 2016-11 | None |
| 2016-12 | 1 |
| 2018-09 | 16 |
| 2018-10 | 4 |

These months have very few orders, so the monthly trend chart is limited to January 2017 – August 2018.

## 5. Reconciliation (BRL)

| Check | Result |
|---|---|
| Delivered payment value (SQL) | 15,422,461.77 |
| Sum of payment mix by type | 15,422,461.77 |
| Sum of monthly delivered payment value (22 months) | 15,422,461.77 |
| Delivered item sales (SUM(price)) | 13,221,498.11 |
| Sum of category_sales.csv after fix | 13,221,498.11 |
| Sum of monthly_orders.csv after fix | 96,478 delivered orders |
| Payment value of all orders | 16,008,872.12 |

The difference between all-order payment value and delivered payment value is R$ 586,410.35, belonging to orders that are not delivered.

## 6. Issue Found and Fixed

The first version of the dashboard export did not filter on delivered orders for two summaries:

- category_sales summed item prices for all orders: 13,591,643.70 instead of 13,221,498.11, a difference of 370,145.59.
- monthly_orders counted all 99,441 orders instead of 96,478 delivered orders.

Both queries in `scripts/export_dashboard_data.py` were changed to filter for delivered orders. The totals now match the reconciliation checks.

The exploratory queries 5 and 8 in `sql/sales_analysis.sql` had the same missing filter and were corrected in a later cleanup.

## 7. Known Limitations

- 610 products have no category name. They are grouped as unknown or by the available name in the category summary.
- A few categories have no English translation (for example `pc_gamer`), so the Portuguese name is kept.
- Delivery-date fields are missing for orders that were not delivered, so delivery-time analysis is limited to delivered orders.
- The average review score is calculated over all reviews and is not filtered by order status.
