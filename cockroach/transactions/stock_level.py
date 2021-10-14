import logging


def stock_level_transaction(
    conn, warehouse_num, district_num, stock_threshold, num_last_orders_to_examine
):
    result = 0
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT COUNT(*)
            FROM 
                Stock AS s
            WHERE 
                s.S_QUANTITY < %s
                AND s.S_I_ID IN 
                    (SELECT OL_I_ID AS item_number
                    FROM 
                        Order AS o 
                        INNER JOIN 
                        Order-Line AS ol
                    ON 
                        o.O_W_ID = ol.OL_W_ID
                        AND o.O_D_ID = ol.OL_D_ID
                        AND o.O_ID = ol.OL_O_ID
                    WHERE
                        o.O_W_ID = %s 
                        AND o.O_D_ID = %s
                    ORDER BY 
                        o.O_ENTRY_D DESC
                    LIMIT 
                        %s);
            """,
            (stock_threshold, warehouse_num, district_num, num_last_orders_to_examine),
        )
        result = cur.fetchone()[0]
        logging.debug(f"stock_level_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
    return result
