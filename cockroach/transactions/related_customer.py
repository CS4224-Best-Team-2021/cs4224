import logging


def related_customer_transaction(conn, customer):
    c_w_id, c_d_id, c_id = customer
    result = None

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                c.c_w_id,
                c.c_d_id,
                c.c_id
            FROM   customer AS c
            WHERE  c.c_w_id != %s EXISTS
                (
                        SELECT 1
                        FROM   ORDER AS o1
                        WHERE  o1.o_w_id = %s
                        AND    o1.o_d_id = %s
                        AND    o1.o_c_id = %s
                        AND    EXISTS
                                (
                                        SELECT 1
                                        FROM   ORDER AS o2
                                        WHERE  o1.o_w_id = c.c_w_id
                                        AND    o1.o_d_id = c.c_d_id
                                        AND    o1.o_c_id = c.c_id
                                        AND    EXISTS
                                            (
                                                    SELECT 1
                                                    FROM   ORDER-line AS ol1
                                                    WHERE  ol1.ol_w_id = o1.o_w_id
                                                    AND    ol1.ol_d_id = o1.o_d_id
                                                    AND    ol1.ol_o_id = o1.o_id
                                                    AND    EXISTS
                                                            (
                                                                    SELECT 1
                                                                    FROM   ORDER-line AS ol2
                                                                    WHERE  ol2.ol_w_id = o1.o_w_id
                                                                    AND ol1.ol_d_id = o1.o_d_id
                                                                    AND ol2.ol_o_id = o1.o_id
                                                                    AND    EXISTS
                                                                        (
                                                                                SELECT 1
                                                                                FROM   ORDER-line AS ol3
                                                                                WHERE  ol3.ol_w_id = o2.o_w_id
                                                                                AND    ol1.ol_d_id = o2.o_d_id
                                                                                AND    ol3.ol_o_id = o2.o_id
                                                                                AND    EXISTS
                                                                                        (
                                                                                                SELECT 1
                                                                                                FROM   ORDER-line AS ol4
                                                                                                WHERE  ol4.ol_w_id = o2.o_w_id
                                                                                                AND    ol1.ol_d_id = o2.o_d_id
                                                                                                AND    ol4.ol_o_id = o2.o_id
                                                                                                AND    ol1.ol_i_id != ol2.ol_i_id
                                                                                                AND    ol3.ol_i_id != ol4.ol_i_id
                                                                                                AND    ol1.ol_i_id = ol3.ol_i_id
                                                                                                AND    ol2.ol_i_id = ol4.ol_i_id ) ) ) ) ) );
            """,
            (c_w_id, c_w_id, c_d_id, c_id),
        )
        result = cur.fetchall()

        logging.debug(
            f"related_customer_transaction(): Status Message {cur.statusmessage}"
        )

    conn.commit()
    return result
