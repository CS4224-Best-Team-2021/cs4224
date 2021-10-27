import logging

IntVector = list[int]

def new_order_transaction(conn, c_w_id, c_d_id, c_id, item_number: IntVector, supplier_warehouse: IntVector, quantity: IntVector):
    # 1. Let N denote value of the next available order number D_NEXT_O_ID for district (W_ID,D_ID)
    result = None
    N = 0
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                d.D_NEXT_O_ID
            FROM
                district AS d
            WHERE
                d.D_W_ID = %s
                AND d.D_ID = %s;
            """,
            (c_w_id, c_d_id),
        )

        result = cur.fetchone()
        N = result[0] + 1

    # 2. Update the district (W ID, D ID) by incrementing D_NEXT_O_ID by one
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE 
                district
            SET 
                D_NEXT_O_DID = D_NEXT_O_DID + 1
            WHERE
                d.D_W_ID = %s
                AND d.D_ID = %s;
            """,
            (c_w_id, c_d_id)
        )
    
    # 3. Create a new order
    O_ALL_LOCAL = 1
    for warehouse in supplier_warehouse:
        if warehouse != c_w_id:
            O_ALL_LOCAL = 0
            break

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO 
                "order" (O_ID, O_D_ID, O_W_ID, O_C_ID, O_ENTRY_D, O_CARRIER_ID, O_OL_CNT, O_ALL_LOCAL)
            VALUES 
                (%s, %s, %s, %s, current_timestamp(), NULL, %s, %s);
            """,
            (N, c_d_id, c_w_id, c_id, len(item_number), O_ALL_LOCAL),
        )
    
    # 4. Initialise total amount to 0
    TOTAL_AMOUNT = 0
    
    # 5. For each item, update the relevant tables
    for i in range(0, len(item_number)):
        # (a) Check stock quantity for the current item
        S_QUANTITY = 0
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    s.S_QUANTITY
                FROM 
                    stock AS s
                WHERE
                    s.S_W_ID = %s
                    AND s.S_I_ID = %s;
                """,
                (supplier_warehouse[i], item_number[i]),
            )

            result = cur.fetchone()
            S_QUANTITY = result[0]
        
        # (b) Calculate adjusted quantity
        ADJUSTED_QTY = S_QUANTITY - quantity[i]

        # (c) If adjusted quantity < 10, set adjusted quantity += 100
        if ADJUSTED_QTY < 10:
            ADJUSTED_QTY += 100

        # (d) Update the stock for the item and warehouse
        S_REMOTE_CNT = 0
        if supplier_warehouse[i] != c_w_id:
            S_REMOTE_CNT = 1

        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE 
                    stock 
                SET
                    S_QUANTITY = %s,
                    S_YTD = S_YTD + %s,
                    S_ORDER_CNT = S_ORDER_CNT + 1, 
                    S_REMOTE_CNT = S_REMOTE_CNT + %s
                WHERE 
                    S_W_ID = %s
                    AND S_I_ID = %s;
                """,
                (ADJUSTED_QTY, quantity[i], S_REMOTE_CNT, supplier_warehouse[i], item_number[i]),
            )

        # (e) Calculate ITEM_AMOUNT
        I_PRICE = 0
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    I_PRICE
                FROM 
                    item
                WHERE
                    I_ID = %s;
                """,
                (item_number[i]),
            )
            result = cur.fetchone()
            I_PRICE = result[0]
            ITEM_AMOUNT = quantity[i] * I_PRICE

        # (f) Update TOTAL_AMOUNT
        TOTAL_AMOUNT += ITEM_AMOUNT

        # (g) Create a new order line
        OL_DIST_INFO = ""
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT %s FROM stock WHERE S_W_ID = %s AND S_I_ID = %s;
                """,
                (district_id_to_string(c_d_id), supplier_warehouse[i], item_number[i]),
            )
            result = cur.fetchone()
            OL_DIST_INFO = result[0]

        # Note that i is 0-indexed in the code but 1-indexed in the project description, so OL_NUMBER should be i + 1 
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO
                    order_line (OL_O_ID, OL_D_ID, OL_W_ID, OL_NUMBER, OL_I_ID, OL_SUPPLY_W_ID, OL_QUANTITY, OL_AMOUNT, OL_DELIVERY_D, OL_DIST_INFO)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, NULL, %s);
                """,
                (N, c_d_id, c_w_id, i + 1, item_number[i], supplier_warehouse[i], quantity[i], ITEM_AMOUNT, OL_DIST_INFO),
            )
    
    # 6. Calculate the total value of this transaction
    W_TAX = 0
    with conn.cursor as cur:
        cur.execute(
            """
            SELECT W_TAX FROM warehouse WHERE W_ID = %s;
            """,
            (c_w_id),
        )
        result = cur.fetchone()
        W_TAX = result[0]

    D_TAX = 0
    with conn.cursor as cur:
        cur.execute(
            """
            SELECT 
                D_TAX 
            FROM
                
            """
        )

def district_id_to_string(id: int):
    """
    Takes id and returns "S_DIST_id", zero-padded to two places.
    """
    if id < 10:
        return "S_DIST_0" + str(id)
    else:
        return "S_DIST_10"