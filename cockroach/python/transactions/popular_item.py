import logging


def popular_item_transaction(
    conn,
    log_buffer,
    test,
    warehouse_number,
    district_number,
    num_last_orders_to_examine,
):
    """
    1. Get items from last L orders at a specified warehouse district   - sort orders by O_ENTRY_D
    2. Get most popular item and details                                -
    """
    result = None
    log_buffer.append(
        f"District identifier (W_ID, D_ID): {warehouse_number},{district_number}"
    )
    log_buffer.append(f"Number of orders to examine: {num_last_orders_to_examine}")

    with conn.cursor() as cur:
        # set S: set of last L orders for district (W_ID, D_ID)
        cur.execute(
            """
            SELECT 
                O_ID, 
                O_ENTRY_D,
                C_FIRST,
                C_MIDDLE,
                C_LAST
            FROM
                "order" AS o
                INNER JOIN 
                customer AS c
                ON 
                    c.C_W_ID = o.O_W_ID 
                    AND c.C_ID = o.O_C_ID 
                    AND c.C_D_ID = o.O_D_ID
            WHERE
                o.O_W_ID = %s 
                AND o.O_D_ID = %s
            ORDER BY 
                o.O_ID DESC
            LIMIT 
                %s
            FOR UPDATE;
            """,
            (warehouse_number, district_number, num_last_orders_to_examine),
        )
        S = cur.fetchall()

        log_buffer.append(f"Orders in S: (O_ID, O_ENTRY_D, C_FIRST, C_MIDDLE, C_LAST)")
        for s in S:
            log_buffer.append(f"    {s}")

        order_ids = tuple([s[0] for s in S])
        popular_item_ids = []

        for order_id in order_ids:
            cur.execute(
                """
                SELECT 
                    (SELECT I_NAME FROM Item AS i WHERE ol1.OL_I_ID = i.I_ID) AS I_NAME,
                    ol1.OL_I_ID,
                    ol1.OL_QUANTITY
                FROM
                    order_line ol1
                WHERE 
                    ol1.OL_W_ID = %s
                    AND ol1.OL_D_ID = %s
                    AND ol1.OL_O_ID = %s
                    AND ol1.OL_QUANTITY >= (
                        SELECT 
                            MAX(ol2.OL_QUANTITY)
                        FROM 
                            order_line ol2
                        WHERE
                            ol2.OL_W_ID = %s
                            AND ol2.OL_D_ID = %s
                            AND ol2.OL_O_ID = %s
                        )
                FOR UPDATE;
                """,
                (
                    warehouse_number,
                    district_number,
                    order_id,
                    warehouse_number,
                    district_number,
                    order_id,
                ),
            )
            popular_items = cur.fetchall()
            log_buffer.append(f"Popular items for {order_id} (I_NAME, OL_QUANTITY):")
            for item in popular_items:
                log_buffer.append(f"    {item}")
            popular_item_ids.extend(list(map(lambda x: x[1], popular_items)))

        cur.execute(
            """
            SELECT
                (SELECT I_NAME FROM Item AS i WHERE ol.OL_I_ID = i.I_ID) AS I_NAME,
                COUNT(DISTINCT(ol.OL_O_ID)) / %s * 100 AS percentage
            FROM
                order_line ol
            WHERE
                ol.OL_W_ID = %s
                AND ol.OL_D_ID = %s
                AND ol.OL_O_ID IN %s
                AND ol.OL_I_ID IN %s
            GROUP BY
                ol.OL_I_ID;
            """,
            (
                num_last_orders_to_examine,
                warehouse_number,
                district_number,
                order_ids,
                tuple(popular_item_ids),
            ),
        )

        result = cur.fetchall()
        log_buffer.append(
            "Percentage of examined orders that contain each popular item (I_NAME, percentage):"
        )
        for r in result:
            log_buffer.append(f"    {r}")

        logging.debug(f"popular_item_transaction(): Status Message {cur.statusmessage}")

