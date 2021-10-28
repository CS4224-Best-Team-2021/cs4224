import logging

def delivery_transaction(conn, w_id, carrier_id):
    for district_no in range(1, 11):
        N = 0
        with conn.cursor() as cur:
            # (a) Find the earliest unfulfilled order
            cur.execute(
                """
                SELECT 
                    MIN(O_ID)
                FROM 
                    "order"
                WHERE
                    (O_W_ID, O_D_ID) = (%s, %s)
                    AND O_CARRIER_ID IS NULL;
                """,
                (w_id, district_no),
            )

            result = cur.fetchone()
            N = result[0]

            # (b) Assign this order to the given carrier
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
            )

            # (c) Update all order-lines in this order
            cur.execute(
                """
                WITH curr_time AS SELECT current_timestamp()
                UPDATE
                    order_line
                SET
                    OL_DELIVERY_D = curr_time
                WHERE
                    (OL_W_ID, OL_D_ID, OL_O_ID) = (%s, %s, %s);
                """,
                (w_id, district_no, N),
            )

            # (d) Update the customer
            O_C_ID = 0 # Get the customer ID
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
            )

            result = cur.fetchone()
            O_C_ID = result[0]
            
            B = 0 
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
            )
            result = cur.fetchone()
            B = result[0]

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
            )

        conn.commit()

