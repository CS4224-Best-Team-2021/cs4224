import logging

def delivery_transaction(conn, log_buffer, test, w_id, carrier_id):
    """
    No output required for this transaction
    """
    for district_no in range(1, 11):
        N = 0
        
        # (a) Find the earliest unfulfilled order for this warehouse and district
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    O_ID
                FROM 
                    "order"
                WHERE
                    O_ID = (
                        SELECT 
                            MIN(O_ID)
                        FROM 
                            "order" 
                        WHERE
                            (O_W_ID, O_D_ID, O_CARRIER_ID) = (%s, %s, NULL)
                    )
                FOR UPDATE;
                """,
                (w_id, district_no),
            ) # uses customer_order index

            result = cur.fetchone()

            # If there is no unfulfilled order, go to the next district
            if result is None:
                continue

            N = result[0]


        # (b) Assign this order to the given carrier
        with conn.cursor() as cur:   
            cur.execute(
                """
                UPDATE
                    "order"
                SET
                    O_CARRIER_ID = %s
                WHERE 
                    (O_W_ID, O_D_ID, O_ID) = (%s, %s, %s);
                """,
                (carrier_id, w_id, district_no, N),
            ) # uses primary key index
        
        conn.commit() # Try committing early to prevent contention

        # (c) Update all order-lines in this order
        with conn.cursor() as cur:
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
                (w_id, district_no, N),
            ) # uses order_index
        
        conn.commit() # Add more intermittent commits to prevent contention

        # (d) Update the customer
        O_C_ID = 0 

        # Get the customer ID
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    O_C_ID
                FROM
                    "order"
                WHERE 
                    (O_W_ID, O_D_ID, O_ID) = (%s, %s, %s);
                """,
                (w_id, district_no, N),
            ) # uses primary key index

            result = cur.fetchone()
            O_C_ID = result[0]

        # Get the sum of OL_AMOUNT for all the items in the order
        B = 0 
        with conn.cursor() as cur:    
            cur.execute(
                """
                SELECT 
                    SUM(OL_AMOUNT)
                FROM
                    order_line
                WHERE
                    (OL_W_ID, OL_D_ID, OL_O_ID) = (%s, %s, %s);
                """,
                (w_id, district_no, N),
            ) # uses order_index

            result = cur.fetchone()
            B = result[0]
        
        # Update C_BALANCE and C_DELIVERY_CNT for the customer
        with conn.cursor() as cur:
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
                (B, w_id, district_no, O_C_ID),
            ) # uses primary key index
        
        conn.commit() # Add more intermittent commits to prevent contention

    conn.commit()
