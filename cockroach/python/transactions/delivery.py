import logging

def delivery_transaction(conn, log_buffer, test, w_id, carrier_id):
    """
    No output required for this transaction
    """
    for district_no in range(1, 11):
        N = 0
        with conn.cursor() as cur:
            # (a) Find the earliest unfulfilled order
            cur.execute(
                """
                SELECT 
                    O_ID
                FROM 
                    "order"
                WHERE
                    (O_W_ID, O_D_ID) = (%s, %s)
                    AND O_CARRIER_ID IS NULL
                ORDER BY O_ID ASC
                LIMIT 1
                FOR UPDATE;
                """,
                (w_id, district_no),
            ) # uses customer_order index

            result = cur.fetchone()

            # If there is no unfulfilled order, go to the next district
            if result is None:
                conn.commit()
                continue

            N = result[0]

            # # If user wants to test this transaction, check that this order really has no carrier
            # if test:
            #     cur.execute(
            #         """
            #         SELECT
            #             O_CARRIER_ID
            #         FROM 
            #             "order"
            #         WHERE
            #             (O_W_ID, O_D_ID, O_ID) = (%s, %s, %s)
            #         FOR UPDATE;
            #         """,
            #         (w_id, district_no, N),
            #     )
            #     result = cur.fetchone()
            #     assert(result[0] is None)
            
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
            ) # uses primary key index
            conn.commit()

            # If user wants to test this transaction, check that this order has the carrier we just assigned
            # if test:
            #     cur.execute(
            #         """
            #         SELECT
            #             O_CARRIER_ID
            #         FROM 
            #             "order"
            #         WHERE
            #             (O_W_ID, O_D_ID, O_ID) = (%s, %s, %s);
            #         """,
            #         (w_id, district_no, N),
            #     )
            #     result = cur.fetchone()
            #     assert(result[0] == carrier_id)

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
                (w_id, district_no, N),
            ) # uses order_index

            # (d) Update the customer
            # Get the customer ID
            O_C_ID = 0 
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
            ) # uses order_index

            result = cur.fetchone()
            B = result[0]

            # If user wants transaction to be tested, get the original c_balance, c_delivery_cnt
            # initial_values = None
            # if test:
            #     cur.execute(
            #         """
            #         SELECT
            #             C_BALANCE, C_DELIVERY_CNT
            #         FROM
            #             customer 
            #         WHERE 
            #             (C_W_ID, C_D_ID, C_ID) = (%s,%s,%s);
            #         """,
            #         (w_id, district_no, O_C_ID),
            #     )
            #     initial_values = cur.fetchone()

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

            # If user wants transaction to be tested, get the original c_balance, c_delivery_cnt
            # if test:
            #     cur.execute(
            #         """
            #         SELECT
            #             C_BALANCE, C_DELIVERY_CNT
            #         FROM
            #             customer 
            #         WHERE 
            #             (C_W_ID, C_D_ID, C_ID) = (%s,%s,%s);
            #         """,
            #         (w_id, district_no, O_C_ID),
            #     )
            #     result = cur.fetchone()
            #     assert(result[0] - initial_values[0] == B)
            #     assert(result[1] - initial_values[1] == 1)

    conn.commit()

