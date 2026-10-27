\# Data Quality Checks



All checks were run on the Olist Brazilian e-commerce dataset after loading it into SQLite (`scripts/load\_data.py`, `scripts/load\_to\_sqlite.py`, `scripts/run\_sql.py`, `scripts/check\_aov.py`).



\## 1. Row Counts, Duplicates and Missing Values



| Table | Rows | Fully Duplicate Rows | Missing Values |

|---|---:|---:|---|

| customers | 99,441 | 0 | None |

| orders | 99,441 | 0 | order\_approved\_at: 160; order\_delivered\_carrier\_date: 1,783; order\_delivered\_customer\_date: 2,965 |

| order\_items | 112,650 | 0 | None |

| order\_payments | 103,886 | 0 | None |

| order\_reviews | 99,224 | 0 | review\_comment\_title: 87,656; review\_comment\_message: 58,247 |

| products | 32,951 | 0 | Category and 3 other text/photo columns: 610 each; 4 size/weight columns: 2 each |

| sellers | 3,095 | 0 | None |

| product\_category\_name\_translation | 71 | 0 | None |



Note: Duplicate rows means completely identical rows. Duplicates by order\_id were not tested separately.



\## 2. Order Status



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

| \*\*Total\*\* | \*\*99,441\*\* |



Delivered rate: 96,478 / 99,441 = 97.02%.



\## 3. Payments



\- The order\_payments table has 103,886 rows for 99,441 orders. Some orders have multiple payment rows, for example installments or vouchers. Order counts should use COUNT(DISTINCT order\_id).

\- One delivered order has no payment record. Delivered orders with a payment record: 96,477 out of 96,478.

\- Average order value (AOV) uses these 96,477 orders.

\- An order can use more than one payment type, so order counts per payment type can add up to more than the number of orders.



\## 4. Incomplete Months



| Month | Orders (All Statuses) |

|---|---:|

| 2016-09 | 4 |

| 2016-10 | 324 |

| 2016-11 | None |

| 2016-12 | 1 |

| 2018-09 | 16 |

| 2018-10 | 4 |



These months have very few orders, so the monthly trend chart is limited to January 2017 – August 2018.



\## 5. Reconciliation (BRL)



| Check | Result |

|---|---|

| Delivered payment value (SQL) | 15,422,461.77 |

| Sum of payment mix by type | 15,422,461.77 |

| Sum of monthly delivered payment value (22 months) | 15,422,461.77 |

| Delivered item sales (SUM(price)) | 13,221,498.11 |

| Sum of category\_sales.csv after fix | 13,221,498.11 |

| Sum of monthly\_orders.csv after fix | 96,478 delivered orders |

| Payment value of all orders | 16,008,872.12 |



The difference between all-order payment value and delivered payment value is R$ 586,410.35, belonging to orders that are not delivered.



\## 6. Issue Found and Fixed



The first version of the dashboard export did not filter on delivered orders for two summaries:



\- category\_sales summed item prices for all orders: 13,591,643.70 instead of 13,221,498.11, a difference of 370,145.59.

\- monthly\_orders counted all 99,441 orders instead of 96,478 delivered orders.



Both queries in scripts/export\_dashboard\_data.py were changed to filter for delivered orders. The totals now match the reconciliation checks.



\## 7. Known Limitations



\- 610 products have no category name. They are grouped as unknown or by the available name in the category summary.

\- Delivery-date fields are missing for orders that were not delivered, so delivery-time analysis is limited to delivered orders.
