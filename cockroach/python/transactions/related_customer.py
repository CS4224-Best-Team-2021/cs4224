import logging


def related_customer_transaction(conn, customer):
    c_w_id, c_d_id, c_id = customer
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            REFRESH MATERIALIZED VIEW related_customer_view;
            SELECT 
                C_W_ID2, C_D_ID2, C_ID2
            FROM 
                related_customer_view
            WHERE
                C_W_ID1 = %s
                AND C_D_ID1 = %s
                AND C_ID1 = %s;
            """,
            (c_w_id, c_w_id, c_d_id, c_id),
        )
        result = cur.fetchall()

        logging.debug(
            f"related_customer_transaction(): Status Message {cur.statusmessage}"
        )

    conn.commit()
    return result
