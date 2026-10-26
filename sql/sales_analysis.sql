
-- 1. Check total number of orders
SELECT COUNT(*) AS total_orders
FROM olist_orders_dataset;

-- 2. Check order status distribution
SELECT
    order_status,
    COUNT(*) AS number_of_orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY number_of_orders DESC;

-- 3. Check total payment value
SELECT
    ROUND(SUM(payment_value), 2) AS total_payment_value
FROM olist_order_payments_dataset;

-- 4. Check top 10 product categories by number of order items
SELECT
    p.product_category_name,
    COUNT(*) AS total_items
FROM olist_order_items_dataset AS oi
JOIN olist_products_dataset AS p
    ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total_items DESC
LIMIT 10;


-- 5. Monthly order volume
SELECT
    strftime('%Y-%m', order_purchase_timestamp) AS month,
    COUNT(*) AS total_orders
FROM olist_orders_dataset
WHERE order_purchase_timestamp IS NOT NULL
GROUP BY month
ORDER BY month;

-- 6. Monthly payment value
SELECT
    strftime('%Y-%m', o.order_purchase_timestamp) AS month,
    ROUND(SUM(p.payment_value), 2) AS total_payment_value
FROM olist_orders_dataset AS o
JOIN olist_order_payments_dataset AS p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
  AND o.order_purchase_timestamp IS NOT NULL
GROUP BY month
ORDER BY month;

-- 7. Order status distribution
SELECT
    order_status,
    COUNT(*) AS total_orders
FROM olist_orders_dataset
GROUP BY order_status
ORDER BY total_orders DESC;

-- 8. Top 10 product categories by item sales value
SELECT
    COALESCE(t.product_category_name_english,
             p.product_category_name,
             'unknown') AS category,
    ROUND(SUM(oi.price), 2) AS item_sales_value
FROM olist_order_items_dataset AS oi
JOIN olist_products_dataset AS p
    ON oi.product_id = p.product_id
LEFT JOIN product_category_name_translation AS t
    ON p.product_category_name = t.product_category_name
GROUP BY category
ORDER BY item_sales_value DESC
LIMIT 10;


-- 1. Total orders vs delivered orders
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT CASE
        WHEN order_status = 'delivered' THEN order_id
    END) AS delivered_orders
FROM olist_orders_dataset;


-- 2. Payment value for delivered orders
SELECT
    ROUND(SUM(p.payment_value), 2) AS delivered_payment_value_brl
FROM olist_order_payments_dataset p
JOIN olist_orders_dataset o
    ON p.order_id = o.order_id
WHERE o.order_status = 'delivered';


-- 3. Delivered-order AOV (payment-based)
SELECT
    ROUND(
        SUM(p.payment_value) /
        NULLIF(COUNT(DISTINCT o.order_id), 0),
        2
    ) AS delivered_payment_aov_brl
FROM olist_orders_dataset o
JOIN olist_order_payments_dataset p
    ON o.order_id = p.order_id
WHERE o.order_status = 'delivered';


-- 4. Item price total, separately from payments
SELECT
    ROUND(SUM(i.price), 2) AS item_sales_value_brl
FROM olist_order_items_dataset i
JOIN olist_orders_dataset o
    ON i.order_id = o.order_id
WHERE o.order_status = 'delivered';


-- 5. Delivered percentage
SELECT
    ROUND(
        100.0 * COUNT(DISTINCT CASE
            WHEN order_status = 'delivered' THEN order_id
        END) / NULLIF(COUNT(DISTINCT order_id), 0),
        2
    ) AS delivered_percentage
FROM olist_orders_dataset;


-- 6. Average review score
SELECT
    ROUND(AVG(review_score), 2) AS average_review_score
FROM olist_order_reviews_dataset;
