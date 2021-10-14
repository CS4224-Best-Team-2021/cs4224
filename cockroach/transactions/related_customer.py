import logging


def related_customer_transaction(conn, customer):
    c_w_id, c_d_id, c_id = customer
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            WITH customer_order_lines AS 
                (
                    SELECT
                        o.O_W_ID, o.O_D_ID, o.O_ID, o.C_ID, ol.OL_I_ID
                    FROM
                        Order o
                        INNER JOIN 
                        Order-Line ol
                    ON
                        o.O_W_ID = ol.OL_W_ID
                        AND o.O_D_ID = ol.OL_D_ID
                        AND o.O_ID = ol.OL_O_ID
                )
            
            SELECT
                col1.C_ID
            FROM
                customer_order_lines AS col1
            WHERE
                EXISTS ()

            """,
            (c_w_id, c_d_id, c_id),
        )
        result = cur.fetchall()

        logging.debug(
            f"related_customer_transaction(): Status Message {cur.statusmessage}"
        )

    conn.commit()
    return result
