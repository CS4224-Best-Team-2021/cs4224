import logging


def order_status_transaction(conn, log_buffer, test, c_w_id, c_d_id, c_id):
    """
    1. Get last order of a customer         - sort orders by O_ENTRY_D
    2. Get order-lines of that last order   - retrieve order lines
    """
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                C_FIRST, C_MIDDLE, C_LAST, C_BALANCE
            FROM
                customer
            WHERE
                C_W_ID = %s
                AND C_D_ID = %s
                AND C_ID = %s;
            """,
            (c_w_id, c_d_id, c_id)
        )
        res = cur.fetchall()[0]
        log_buffer.append(f'Customer name and balance (C_FIRST, C_MIDDLE, C_LAST, C_BALANCE): {res}')

        cur.execute(
            """
            SELECT
                o.O_ID, o.O_ENTRY_D, o.O_CARRIER_ID
            FROM
                "order" as o
            WHERE
                o.O_W_ID = %s
                AND o.O_D_ID = %s
                AND o.O_C_ID = %s
            ORDER BY
                o.O_ID DESC
            LIMIT 1;
            """,
            (c_w_id, c_d_id, c_id),
        )

        last_order = cur.fetchone()
        log_buffer.append(f'Customer last order (O_ID, O_ENTRY_D, O_CARRIER_ID): {last_order}')
        o_id = last_order[0]

        cur.execute(
            """
            SELECT 
                OL_I_ID, OL_SUPPLY_W_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D
            FROM 
                order_line
            WHERE 
                OL_W_ID = %s
                AND OL_D_ID = %s
                AND OL_O_ID = %s;
            """,
            (c_w_id, c_d_id, o_id),
        )

        order_lines = cur.fetchall()
        log_buffer.append('Items in last order: (OL_I_ID, OL_SUPPLY_W_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D)')
        for o in order_lines:
            log_buffer.append(f'    {o}')

        logging.debug(f"order_status_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
