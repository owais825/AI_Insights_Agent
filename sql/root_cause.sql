-- =========================================
-- SELLER RISK SEGMENTATION WITH CATEGORIES
-- =========================================

SELECT *,
    CASE 
	    WHEN avg_late_delay_days > 15 THEN 'Critical'
	    WHEN late_pct > 40 THEN 'High Risk'
	    WHEN late_pct > 25 THEN 'Inconsistent'
	    ELSE 'Normal'
		END AS seller_category

FROM (
    SELECT
        seller_id,
        COUNT(*) AS total_orders,

        AVG(EXTRACT(EPOCH FROM delivery_delay) / 86400) AS avg_delay_days,

        SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_pct,

        AVG(
            CASE 
                WHEN delivery_status = 'Late' 
                THEN EXTRACT(EPOCH FROM delivery_delay) / 86400
            END
        ) AS avg_late_delay_days

    FROM delivery_base
    GROUP BY seller_id
) t

WHERE total_orders > 20
AND late_pct > 25

ORDER BY late_pct DESC;