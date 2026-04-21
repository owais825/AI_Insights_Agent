from mcp_server.core.db import get_connection
from mcp_server.core.sql_validator import validate_sql
from mcp_server.core.result_validator import validate_result


def convert_decimal(value):
    from decimal import Decimal
    if isinstance(value, Decimal):
        return round(float(value), 2)
    return value


def get_delivery_kpis():
    """
    Returns overall delivery performance KPIs:
    - total orders
    - late %, on-time %, early %
    - avg delay (days)
    """

    query = """
    SELECT
        COUNT(*) AS total_orders,

        SUM(CASE WHEN delivery_status = 'Late' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS late_pct,

        SUM(CASE WHEN delivery_status = 'On Time' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS on_time_pct,

        SUM(CASE WHEN delivery_status = 'Early' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS early_pct,

        AVG(EXTRACT(EPOCH FROM delivery_delay) / 86400) AS avg_delay_days

    FROM delivery_base;
    """

    # Validate SQL
    validate_sql(query)

    # Execute
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)

    columns = [desc[0] for desc in cursor.description]
    row = cursor.fetchone()

    result = {col: convert_decimal(val) for col, val in zip(columns, row)}

    # Validate result
    validate_result([result])

    cursor.close()
    conn.close()

    return result