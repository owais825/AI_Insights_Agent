-- =========================================
-- =========================================
-- DELIVERY KPI SUMMARY
-- =========================================

SELECT
    COUNT(*) AS total_orders,

    -- Late %
    SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_pct,

    -- On Time %
    SUM(CASE WHEN delivery_status = 'On Time' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS on_time_pct,

    -- Early %
    SUM(CASE WHEN delivery_status = 'Early' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS early_pct,

    -- Average Delay (in days)
    AVG(EXTRACT(EPOCH FROM delivery_delay) / 86400) AS avg_delay_days,

    -- % of orders delayed more than 7 days
    SUM(
    CASE 
        WHEN EXTRACT(EPOCH FROM delivery_delay)/86400 > 7 THEN 1 
        ELSE 0 
    END
        ) * 100.0 / COUNT(*) AS severe_delay_pct

FROM delivery_base;