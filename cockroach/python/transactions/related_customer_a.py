import logging


def a_related_customer_transaction(conn, log_buffer, test, c_w_id, c_d_id, c_id):
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                C_W_ID2, C_D_ID2, C_ID2
            FROM 
                (SELECT DISTINCT
                    c1.C_W_ID AS C_W_ID1, 
                    c1.C_D_ID AS C_D_ID1, 
                    c1.C_ID AS C_ID1, 
                    c2.C_W_ID AS C_W_ID2, 
                    c2.C_D_ID AS C_D_ID2, 
                    c2.C_ID AS C_ID2
                FROM
                    customer AS c1,
                    customer AS c2,
                    "order" AS o1,
                    "order" AS o2,
                    order_line AS ol1,
                    order_line AS ol2,
                    order_line AS ol3,
                    order_line AS ol4
                WHERE 
                    -- c1 and c2 in different warehouses
                    c1.C_W_ID != c2.C_W_ID
                    -- c1 has o1
                    AND c1.C_W_ID = o1.O_W_ID
                    AND c1.C_D_ID = o1.O_D_ID
                    AND c1.C_ID = o1.O_C_ID
                    -- c2 has o2
                    AND c2.C_W_ID = o2.O_W_ID
                    AND c2.C_D_ID = o2.O_D_ID
                    AND c2.C_ID = o2.O_C_ID
                    -- ol1 and ol2 in o1
                    AND  ol1.OL_W_ID = o1.O_W_ID
                    AND  ol1.OL_D_ID = o1.O_D_ID
                    AND  ol1.OL_O_ID = o1.O_ID
                    AND  ol2.OL_W_ID = o1.O_W_ID
                    AND  ol2.OL_D_ID = o1.O_D_ID
                    AND  ol2.OL_O_ID = o1.O_ID
                    -- ol3 and ol4 are in o2
                    AND  ol3.OL_W_ID = o2.O_W_ID
                    AND  ol3.OL_D_ID = o2.O_D_ID
                    AND  ol3.OL_O_ID = o2.O_ID
                    AND  ol4.OL_W_ID = o2.O_W_ID
                    AND  ol4.OL_D_ID = o2.O_D_ID
                    AND  ol4.OL_O_ID = o2.O_ID
                    -- OL1 and OL2 are not the same items
                    AND ol1.OL_I_ID != ol2.OL_I_ID 
                    -- OL3 and OL4 are not the same items
                    AND ol3.OL_I_ID != ol4.OL_I_ID 
                    -- OL1 and OL3 are the same items
                    AND ol1.OL_I_ID = ol3.OL_I_ID 
                    -- OL2 and OL4 are the same items
                    AND ol2.OL_I_ID = ol4.OL_I_ID) AS c
            WHERE
                C_W_ID1 = %s
                AND C_D_ID1 = %s
                AND C_ID1 = %s;
            """,
            (c_w_id, c_d_id, c_id),
        )
        result = cur.fetchall()
        log_buffer.append("Related customers (C_W_ID, C_D_ID, C_ID):")
        for c in result:
            log_buffer.append(f"    {c}")

        logging.debug(
            f"related_customer_transaction(): Status Message {cur.statusmessage}"
        )

    conn.commit()
