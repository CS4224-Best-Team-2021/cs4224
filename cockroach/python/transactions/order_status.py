import logging


def order_status_transaction(conn, c_w_id, c_d_id, c_id):
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                o.O_ID, o.O_ENTRY_D, o.O_CARRIER_ID
            FROM
                Order as o
            WHERE
                o.O_W_ID = %s
                AND o.O_D_ID = %s
                AND o.O_C_ID = %s
            ORDER BY
                o.O_ENTRY_D DESC
            LIMIT 1
            """,
            (c_w_id, c_d_id, c_id),
        )

        result = cur.fetchall()
        o_id = result

        cur.execute(
            """
            SELECT 
                OL_I_ID, OL_SUPPLY_W_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D
            FROM 
                Order-Line
            WHERE 
                OL_W_ID = %s
                AND OL_D_ID = %s
                AND OL_O_ID = %s
            """,
            (c_w_id, c_d_id, o_id)
        )
        logging.debug(f"order_status_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
    return result
