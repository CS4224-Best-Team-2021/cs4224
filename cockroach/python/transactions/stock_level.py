import logging


def stock_level_transaction(
    conn, log_buffer, test, warehouse_num, district_num, stock_threshold, num_last_orders_to_examine
):
    """
    1. Get items from last L orders at a specified warehouse district               - sort orders by O_ENTRY_D
    2. Get number of those items that have stock level below a given threshold      - items in orders
    """
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
                        "order" o
                    WHERE
                        o.O_W_ID = %s 
                        AND o.O_D_ID = %s
                    ORDER BY 
                        o.O_ID DESC
                    LIMIT 
                        %s
                    FOR UPDATE
                )

            SELECT 
                COUNT(*)
            FROM 
                Stock AS s
            WHERE 
                s.S_QUANTITY < %s
                AND s.S_W_ID = %s
                AND s.S_I_ID IN 
                    (
                        SELECT
                            ol.OL_I_ID
                        FROM 
                            last_l_orders l
                            INNER JOIN
                            order_line ol
                        ON
                            l.O_W_ID = ol.OL_W_ID
                            AND l.O_D_ID = ol.OL_D_ID
                            AND l.O_ID = ol.OL_O_ID
                    );
            """,
            (warehouse_num, district_num, num_last_orders_to_examine, stock_threshold, warehouse_num),
        )
        result = cur.fetchone()[0]
        log_buffer.append(f'Stock level: {result}')
        logging.debug(f"stock_level_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
