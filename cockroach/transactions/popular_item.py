import logging


def popular_item_transaction(
    conn, warehouse_number, district_number, num_last_orders_to_examine
):
    result = None
    with conn.cursor() as cur:
        cur.execute(
            """
            WITH last_l_order_item_quantities AS
                (
                    SELECT 
                        o.O_W_ID, o.O_D_ID, o.O_ID, ol.OL_I_ID, ol.OL_QUANTITY
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
                        %s
                )
                
            SELECT 
                l1.OL_I_ID, l1.OL_QUANTITY
            FROM
                last_l_order_item_quantities AS l1
            WHERE l1.OL_QUANTITY >= (
                SELECT 
                    MAX(l2.OL_QUANTITY)
                FROM 
                    last_l_order_item_quantities AS l2
                WHERE
                    l1.O_W_ID = l2.O_W_ID
                    AND l1.O_D_ID = l2.O_D_ID
                    AND l1.O_ID = l2.O_ID
            );
            """,
            (warehouse_number, district_number, num_last_orders_to_examine),
        )
        result = cur.fetchall()
        logging.debug(f"popular_item_transaction(): Status Message {cur.statusmessage}")

    # TODO: The question wants us to output a lot more information than just the result
    conn.commit()
    return result
