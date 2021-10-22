import logging


def top_balance_transaction(conn):
    """
    1. Get top 10 customers in descending order of their outstanding balance payments
    """
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            REFRESH MATERIALIZED VIEW top_balance;
            SELECT * FROM top_balance;
            """
        )
        result = cur.fetchall()
        logging.debug(f"top_balance_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
    return result
