# Metric Definitions

Currency: Brazilian Real (BRL, R$). Period: September 2016 to October 2018. The monthly trend chart shows January 2017 – August 2018.

## Key Metrics

| Metric | Definition | Value |
|---|---|---:|
| Total orders | All rows in the orders table, any status | 99,441 |
| Delivered orders | Orders with order_status = 'delivered' | 96,478 |
| Delivered rate | Delivered orders divided by total orders | 97.02% |
| Delivered payment value | Sum of payment_value for delivered orders | R$ 15,422,461.77 |
| Average order value (AOV) | Delivered payment value divided by delivered orders with a payment record | R$ 159.86 |
| Delivered item sales value | Sum of item price for delivered orders, excluding freight | R$ 13,221,498.11 |
| Average review score | Average review_score over all reviews (not filtered by order status) | 4.09 / 5 |

## AOV

R$ 15,422,461.77 / 96,477 = R$ 159.86.

One delivered order has no payment record, so it is excluded from the denominator. Dividing by 96,478 would give R$ 159.85.

## Payment Mix (Delivered Orders)

| Payment Type | Payment Value (R$) | Share |
|---|---:|---:|
| credit_card | 12,101,094.88 | 78.46% |
| boleto | 2,769,932.58 | 17.96% |
| voucher | 343,013.19 | 2.22% |
| debit_card | 208,421.12 | 1.35% |
| **Total** | **15,422,461.77** | **100%** |

Boleto is a Brazilian bank-slip payment method.

## Two Different Sales Measures

The dashboard uses payment value in KPI cards and the payment mix, and item sales value in the category chart.

These are different measures:

- Item sales value is the sum of item prices only.
- Payment value is the amount recorded in customer payment records.

Therefore, R$ 15.42 million and R$ 13.22 million are not expected to match.

## Filters

- The delivered-order KPIs, the monthly trend, the payment mix and the category chart use delivered orders only.
- The average review score uses all reviews.
- Category names use the English translation table where available.
