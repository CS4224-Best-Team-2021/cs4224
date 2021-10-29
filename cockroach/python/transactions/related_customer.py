import logging


def related_customer_transaction(conn, log_buffer, c_w_id, c_d_id, c_id):
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                C_W_ID2, C_D_ID2, C_ID2
            FROM 
                related_customer_view
            WHERE
                C_W_ID1 = %s
                AND C_D_ID1 = %s
                AND C_ID1 = %s;
            """,
            (c_w_id, c_d_id, c_id),
        )
        result = cur.fetchall()
        log_buffer.append('Related customers (C_W_ID, C_D_ID, C_ID):')
        for c in result:
            log_buffer.append(f'    {c}')

        logging.debug(
            f"related_customer_transaction(): Status Message {cur.statusmessage}"
        )

    conn.commit()
    return result
