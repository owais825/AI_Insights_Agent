from mcp_server.core.db import get_connection
from mcp_server.core.sql_validator import validate_sql
from mcp_server.core.result_validator import validate_result


def get_seller_risk_segments(min_orders: int = 20, late_threshold: float = 25.0):
    """
    Returns seller-level risk segmentation based on:
    - late delivery percentage
    - delay severity
    """

    query = f"""
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
    WHERE total_orders > {min_orders}
    AND late_pct > {late_threshold}
    ORDER BY late_pct DESC
    LIMIT 10;
    """

    # ✅ Validate SQL (safety layer)
    validate_sql(query)

    # ✅ Execute query
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()

    def convert_decimal(value):
        from decimal import Decimal
        if isinstance(value, Decimal):
            return float(value)
        return value


    result = [
        {col: convert_decimal(val) for col, val in zip(columns, row)}
        for row in rows
    ]

    # ✅ Validate result
    validate_result(result)

    cursor.close()
    conn.close()

    return result