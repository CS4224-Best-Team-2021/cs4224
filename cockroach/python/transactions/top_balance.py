import logging


def top_balance_transaction(conn, log_buffer, test):
    """
    1. Get top 10 customers in descending order of their outstanding balance payments
    """
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT * FROM top_balance;
            """
        )
        result = cur.fetchall()
        log_buffer.append('In descending order of C_BALANCE (C_FIRST, C_MIDDLE, C_LAST, C_BALANCE, W_NAME, D_NAME):')
        for i in result:
            log_buffer.append(f'    {i}')
        logging.debug(f"top_balance_transaction(): Status Message {cur.statusmessage}")

    conn.commit()

