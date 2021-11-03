import logging

def delivery_transaction(conn, log_buffer, test, w_id, carrier_id):
    """
    No output required for this transaction
    """
    for district_no in range(1, 11):
        deliver_to_one_district(conn, w_id, carrier_id, district_no)


def deliver_to_one_district(conn, w_id, carrier_id, d_id):
    with conn.cursor() as cur:
        # (a - b) Find the earliest unfulfilled order for this warehouse and district and assign this order to the given carrier
        cur.execute(
            """
            UPDATE
                "order"
            SET
                O_CARRIER_ID = %s
            WHERE
                O_ID = (
                    SELECT 
                        O_ID
                    FROM
                        "order"
                    WHERE
                        O_W_ID = %s
                        AND O_D_ID = %s
                        AND O_CARRIER_ID IS NULL
                    ORDER BY
                        O_ID ASC
                    LIMIT 1
                    FOR UPDATE
                )
            RETURNING 
                O_ID;
            """,
            (carrier_id, w_id, d_id),
        )
        conn.commit()
        result = cur.fetchone()

        # If there is no unfulfilled order, return early
        if result is None:
            logging.info(f"No unfulfilled order for w_id = {w_id}, carrier_id = {carrier_id}, d_id = {d_id}")
            return

        N = result[0]
        
        # (c) Update all order-lines in this order
        cur.execute(
            """
            WITH curr_time AS (SELECT current_timestamp::timestamp)
            UPDATE
                order_line
            SET
                OL_DELIVERY_D = (SELECT * FROM curr_time)
            WHERE
                (OL_W_ID, OL_D_ID, OL_O_ID) = (%s, %s, %s);
            """,
            (w_id, d_id, N),
        ) # uses order_index

        conn.commit()

        # (d) Update the customer
        # Get the customer ID
        cur.execute(
            """
            SELECT 
                O_C_ID
            FROM
                "order"
            WHERE 
                (O_W_ID, O_D_ID, O_ID) = (%s, %s, %s);
            """,
            (w_id, d_id, N),
        ) # uses primary key index

        result = cur.fetchone()
        O_C_ID = result[0]

        # Get the sum of OL_AMOUNT for all the items in the order
        cur.execute(
            """
            SELECT 
                SUM(OL_AMOUNT)
            FROM
                order_line
            WHERE
                (OL_W_ID, OL_D_ID, OL_O_ID) = (%s, %s, %s);
            """,
            (w_id, d_id, N),
        ) # uses order_index

        result = cur.fetchone()
        B = result[0]
        
        # Update C_BALANCE and C_DELIVERY_CNT for the customer
        cur.execute(
            """
            UPDATE
                customer
            SET
                C_BALANCE = C_BALANCE + %s,
                C_DELIVERY_CNT = C_DELIVERY_CNT + 1
            WHERE
                (C_W_ID, C_D_ID, C_ID) = (%s, %s, %s);
            """,
            (B, w_id, d_id, O_C_ID),
        ) # uses primary key index

        conn.commit()
    