import logging


def related_customer_transaction(conn, customer):
    c_w_id, c_d_id, c_id = customer
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                c.C_W_ID,
                c.C_D_ID,
                c.C_ID
            FROM   customer AS c
            WHERE  c.C_W_ID != %s EXISTS
                (
                        SELECT 1
                        FROM   ORDER AS o1
                        WHERE  o1.O_W_ID = %s
                        AND    o1.O_D_ID = %s
                        AND    o1.O_C_ID = %s
                        AND    EXISTS
                                (
                                        SELECT 1
                                        FROM   ORDER AS o2
                                        WHERE  o1.O_W_ID = c.C_W_ID
                                        AND    o1.O_D_ID = c.C_D_ID
                                        AND    o1.O_C_ID = c.C_ID
                                        AND    EXISTS
                                            (
                                                    SELECT 1
                                                    FROM   ORDER-line AS ol1
                                                    WHERE  ol1.OL_W_ID = o1.O_W_ID
                                                    AND    ol1.OL_D_ID = o1.O_D_ID
                                                    AND    ol1.OL_O_ID = o1.OL_O_ID
                                                    AND    EXISTS
                                                            (
                                                                    SELECT 1
                                                                    FROM   ORDER-line AS ol2
                                                                    WHERE  ol2.OL_W_ID = o1.O_W_ID
                                                                    AND ol1.OL_D_ID = o1.O_D_ID
                                                                    AND ol2.OL_O_ID = o1.OL_O_ID
                                                                    AND    EXISTS
                                                                        (
                                                                                SELECT 1
                                                                                FROM   ORDER-line AS ol3
                                                                                WHERE  ol3.OL_W_ID = o2.O_W_ID
                                                                                AND    ol1.OL_D_ID = o2.O_D_ID
                                                                                AND    ol3.OL_O_ID = o2.OL_O_ID
                                                                                AND    EXISTS
                                                                                        (
                                                                                                SELECT 1
                                                                                                FROM   ORDER-line AS ol4
                                                                                                WHERE  ol4.OL_W_ID = o2.O_W_ID
                                                                                                AND    ol1.OL_D_ID = o2.O_D_ID
                                                                                                AND    ol4.OL_O_ID = o2.OL_O_ID
                                                                                                AND    ol1.OL_I_ID != ol2.OL_I_ID
                                                                                                AND    ol3.OL_I_ID != ol4.OL_I_ID
                                                                                                AND    ol1.OL_I_ID = ol3.OL_I_ID
                                                                                                AND    ol2.OL_I_ID = ol4.OL_I_ID ) ) ) ) ) );
            """,
            (c_w_id, c_w_id, c_d_id, c_id),
        )
        result = cur.fetchall()

        logging.debug(
            f"related_customer_transaction(): Status Message {cur.statusmessage}"
        )

    conn.commit()
    return result
