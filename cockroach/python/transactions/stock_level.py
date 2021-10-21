import logging


def stock_level_transaction(
    conn, warehouse_num, district_num, stock_threshold, num_last_orders_to_examine
):
    result = 0

    with conn.cursor() as cur:
        # set S: set of last L orders for district (W_ID, D_ID)
        cur.execute(
            """
            WITH last_l_orders AS 
                (
                    SELECT 
                        O_W_ID, O_D_ID, O_ID
                    FROM
                        Order o
                    WHERE
                        o.O_W_ID = %s 
                        AND o.O_D_ID = %s
                    ORDER BY 
                        o.O_ENTRY_D DESC
                    LIMIT 
                        %s
                )

            SELECT 
                COUNT(*)
            FROM 
                Stock AS s
            WHERE 
                s.S_QUANTITY < %s
                AND s.S_I_ID IN 
                    (
                        SELECT
                            ol.OL_I_ID
                        FROM 
                            last_l_orders l
                            INNER JOIN
                            Order-Line ol
                        ON
                            l.O_W_ID = ol.OL_W_ID
                            AND l.O_D_ID = ol.OL_D_ID
                            AND l.O_ID = ol.OL_O_ID
                    );
            """,
            (warehouse_num, district_num, stock_threshold, num_last_orders_to_examine),
        )
        result = cur.fetchone()[0]
        logging.debug(f"stock_level_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
    return result
