import logging


def top_balance_transaction(conn, log_buffer, test):
    """
    1. Get top 10 customers in descending order of their outstanding balance payments
    """
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                c.C_FIRST,
                c.C_MIDDLE,
                c.C_LAST,
                c.C_BALANCE,
                (SELECT W_NAME FROM Warehouse AS w WHERE w.W_ID = c.C_W_ID) AS Warehouse_Name,
                (SELECT D_NAME FROM District AS d WHERE d.D_ID = c.C_D_ID AND d.D_W_ID = c.C_W_ID) AS District_Name
            FROM 
                Customer AS c
            ORDER BY
                c.C_BALANCE DESC
            LIMIT 10;
            """
        )
        result = cur.fetchall()
        log_buffer.append(
            "In descending order of C_BALANCE (C_FIRST, C_MIDDLE, C_LAST, C_BALANCE, W_NAME, D_NAME):"
        )
        for i in result:
            log_buffer.append(f"    {i}")
        logging.debug(f"top_balance_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
