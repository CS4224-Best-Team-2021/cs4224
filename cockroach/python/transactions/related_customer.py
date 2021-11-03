import logging


def related_customer_transaction(conn, log_buffer, test, c_w_id, c_d_id, c_id):
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                O_ID 
            FROM 
                "order"
            WHERE 
                O_W_ID = %s
                AND O_D_ID = %s
                AND O_C_ID = %s
            FOR UPDATE;
            """,
            (c_w_id, c_d_id, c_id),
        )
        order_ids = tuple(cur.fetchall())
        order_map = {}

        for order_id in order_ids:
            cur.execute(
                """
                SELECT
                    OL_I_ID
                FROM
                    order_line
                WHERE
                    OL_W_ID = %s
                    AND OL_D_ID = %s
                    AND OL_O_ID = %s
                FOR UPDATE;
                """,
                (c_w_id, c_d_id, order_id),
            )
            order_map[order_id] = tuple(cur.fetchall())

        related_orders = []
        for order_id, order_set in order_map.items():
            cur.execute(
                """
                SELECT
                    ol1.OL_W_ID,
                    ol1.OL_D_ID,
                    ol1.OL_O_ID
                FROM
                    order_line ol1
                    INNER JOIN 
                    order_line ol2
                ON 
                    -- Order lines are items in this order
                    ol1.OL_I_ID IN %s
                    AND ol2.OL_I_ID IN %s
                    -- Order lines are not the same items
                    AND ol1.OL_I_ID != ol2.OL_I_ID
                    -- Order lines are from the same order
                    AND ol1.OL_O_ID = ol2.OL_O_ID
                    AND ol1.OL_W_ID = ol2.OL_W_ID
                    AND ol1.OL_D_ID = ol2.OL_D_ID
                    AND ol1.OL_W_ID != %s
                FOR UPDATE;
                """,
                (order_set, order_set, c_w_id),
            )
            related_orders.extend(cur.fetchall())

        result = set()
        for related_order in related_orders:
            cur.execute(
                """
                SELECT
                    O_W_ID,
                    O_D_ID,
                    O_C_ID
                FROM
                    "order"
                WHERE
                    O_W_ID = %s
                    AND O_D_ID = %s
                    AND O_ID = %s
                FOR UPDATE;
                """,
                tuple(related_order),
            )
            for res in cur.fetchall():
                result.add(res)

        log_buffer.append("Related customers (C_W_ID, C_D_ID, C_ID):")
        for c in result:
            log_buffer.append(f"    {c}")

        logging.debug(
            f"related_customer_transaction(): Status Message {cur.statusmessage}"
        )
    
    conn.commit()

