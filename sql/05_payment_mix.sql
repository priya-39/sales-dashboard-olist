
-- File: sql/05_payment_mix.sql
-- Purpose: Analyze payment methods for delivered orders.
-- Reconciliation: Total payment value should be BRL 15,422,461.77.

SELECT
    p.payment_type,
    COUNT(DISTINCT p.order_id) AS orders,
    ROUND(SUM(p.payment_value), 2) AS payment_value
FROM olist_order_payments_dataset AS p
JOIN olist_orders_dataset AS o
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
GROUP BY p.payment_type
ORDER BY payment_value DESC;
