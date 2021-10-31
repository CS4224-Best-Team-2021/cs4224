import logging

def payment_transaction(conn, log_buffer, test, c_w_id, c_d_id, c_id, payment):
    # Convert the id's back into ints
    c_w_id = int(c_w_id)
    c_d_id = int(c_d_id)
    c_id = int(c_id)

    # If user wants transaction to be tested, get the original c_balance, c_ytd_payment, c_payment_cnt
    initial_values = None
    if test:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT
                FROM
                    customer 
                WHERE 
                    (C_W_ID, C_D_ID, C_ID) = (%s,%s,%s);
                """,
                (c_w_id, c_d_id, c_id),
            )
            initial_values = cur.fetchone()

    with conn.cursor() as cur:
        # 1. Update the warehouse C_W_ID by incrementing W_YTD by payment
        cur.execute(
            """
            UPDATE 
                warehouse
            SET
                W_YTD = W_YTD + %s
            WHERE 
                W_ID = %s;
            """,
            (payment, c_w_id),
        )

        # 2. Update the district (C_W_ID, C_D_ID) by incrementing D_YTD by payment
        cur.execute(
            """
            UPDATE
                district
            SET
                D_YTD = D_YTD + %s
            WHERE
                (D_W_ID, D_ID) = (%s, %s);
            """,
            (payment, c_w_id, c_d_id),
        )

        # 3. Update the customer
        cur.execute(
            """
            UPDATE
                customer
            SET 
                C_BALANCE = C_BALANCE - %s,
                C_YTD_PAYMENT = C_YTD_PAYMENT + %s,
                C_PAYMENT_CNT = C_PAYMENT_CNT + 1
            WHERE
                (C_W_ID, C_D_ID, C_ID) = (%s, %s, %s);
            """,
            (payment, payment, c_w_id, c_d_id, c_id),
        )

        # If user wanted transaction to be tested, check the new values of c_balance, c_ytd_payment, c_payment_cnt
        if test:
            cur.execute(
                """
                SELECT
                    C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT
                FROM
                    customer 
                WHERE 
                    (C_W_ID, C_D_ID, C_ID) = (%s,%s,%s);
                """,
                (c_w_id, c_d_id, c_id),
            )
            result = cur.fetchone()
            # Check c_balance
            assert(initial_values[0] - result[0] == payment)
            # Check c_ytd_payment
            assert(result[1] - initial_values[1] == payment)
            # Check c_payment_count
            assert(result[2] - initial_values[2] == 1)

        # Generate report
        cur.execute(
            """
            SELECT 
                C_W_ID, C_D_ID, C_ID, C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_BALANCE
            FROM
                customer
            WHERE
                (C_W_ID, C_D_ID, C_ID) = (%s, %s, %s);
            """,
            (c_w_id, c_d_id, c_id),
        )
        result = cur.fetchone()
        
        # 1. Customer's identifier
        log_buffer.append(f"Customer info: {result}")

        cur.execute(
            """
            SELECT 
                W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP
            FROM
                warehouse
            WHERE
                W_ID = %s;
            """,
            (c_w_id,),
        )
        result = cur.fetchone()
        
        # 2. Warehouse's address
        log_buffer.append(f"Warehouse's address: {result}")

        
        cur.execute(
            """
            SELECT 
                D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP
            FROM
                district
            WHERE
                (D_W_ID, D_ID) = (%s, %s);
            """,
            (c_w_id, c_d_id),
        )
        result = cur.fetchone()

        # 3. District's address
        log_buffer.append(f"District's address: {result}")

        # 4. Payment amount
        log_buffer.append(f"Payment amount: {payment}")
    
    conn.commit()
