import logging


def popular_item_transaction(
    conn, warehouse_number, district_number, num_last_orders_to_examine
):
    """
    1. Get items from last L orders at a specified warehouse district   - sort orders by O_ENTRY_D
    2. Get most popular item and details                                -
    """
    result = None

    with conn.cursor() as cur:
        # set S: set of last L orders for district (W_ID, D_ID)
        cur.execute(
            """
            SELECT 
                O_ID, 
                O_ENTRY_D,
                (SELECT C_FIRST FROM Customer AS c WHERE c.C_ID = o.O_C_ID) AS C_FIRST,
                (SELECT C_MIDDLE FROM Customer AS c WHERE c.C_ID = o.O_C_ID) AS C_MIDDLE,
                (SELECT C_LAST FROM Customer AS c WHERE c.C_ID = o.O_C_ID) AS C_LAST
            FROM
                Order o
            WHERE
                o.O_W_ID = %s 
                AND o.O_D_ID = %s
            ORDER BY 
                o.O_ENTRY_D DESC
            LIMIT 
                %s
            """,
            (warehouse_number, district_number, num_last_orders_to_examine),
        )
        S = cur.fetchall()

        # set of popular items, Px
        cur.execute(
            """
            DROP VIEW IF EXISTS last_l_orders;
            CREATE TEMP VIEW last_l_orders (O_W_ID, O_D_ID, _ID)
            AS SELECT 
                    O_W_ID, O_D_ID, O_ID
                FROM
                    Order o
                WHERE
                    o.O_W_ID = %s 
                    AND o.O_D_ID = %s
                ORDER BY 
                    o.O_ENTRY_D DESC
                LIMIT 
                    %s;
            
            DROP VIEW IF EXISTS last_l_order_item_quantities;
            CREATE TEMP VIEW last_l_order_item_quantities (O_W_ID, O_D_ID, O_ID, OL_I_ID, OL_QUANTITY)
            AS SELECT
                    o.O_W_ID, o.O_D_ID, o.O_ID, ol.OL_I_ID, ol.OL_QUANTITY
                FROM 
                    last_l_orders l
                    INNER JOIN
                    Order-Line ol
                ON
                    l.O_W_ID = ol.OL_W_ID
                    AND l.O_D_ID = ol.OL_D_ID
                    AND l.O_ID = ol.OL_O_ID;
                
            SELECT 
                (SELECT I_NAME FROM Item AS i WHERE l1.OL_I_ID = i.I_ID) AS I_NAME,
                l1.OL_I_ID,
                l1.OL_QUANTITY
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
        popular_items = cur.fetchall()
        popular_item_ids = tuple(map(lambda x: x[1], popular_items))

        cur.execute(
            """
            SELECT
                (SELECT I_NAME FROM Item AS i WHERE l1.OL_I_ID = i.I_ID) AS I_NAME,
                COUNT(DISTINCT l.O_W_ID, l.O_D_ID, l.O_ID) / %s * 100 AS percentage
            FROM
                last_l_order_item_quantities AS l
            WHERE 
                l.OL_I_ID IN %s
            GROUP BY
                l.OL_I_ID;
            """,
            popular_item_ids,
            num_last_orders_to_examine,
        )

        logging.debug(f"popular_item_transaction(): Status Message {cur.statusmessage}")

    conn.commit()
    return result
