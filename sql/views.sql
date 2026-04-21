-- =========================================
-- DELIVERY BASE VIEW (Core Analytics Layer)
-- =========================================

CREATE OR REPLACE VIEW delivery_base AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_state,

    oi.seller_id,
    s.seller_state,

    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,

    -- Core Metric
    (o.order_delivered_customer_date - o.order_estimated_delivery_date) 
        AS delivery_delay,

    -- Status Flag (VERY useful later)
    CASE 
        WHEN o.order_delivered_customer_date > o.order_estimated_delivery_date THEN 'Late'
        WHEN o.order_delivered_customer_date >= o.order_estimated_delivery_date - INTERVAL '1 day'
            AND o.order_delivered_customer_date <= o.order_estimated_delivery_date THEN 'On Time'
        ELSE 'Early'
    END AS delivery_status,

    -- Revenue Components
    oi.price,
    oi.freight_value,
    (oi.price + oi.freight_value) AS total_value

FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN sellers s ON oi.seller_id = s.seller_id

-- Only completed deliveries (important)
WHERE o.order_delivered_customer_date IS NOT NULL;