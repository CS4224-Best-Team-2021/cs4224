import logging
from psycopg2 import sql
from typing import List

IntVector = List[int]

def new_order_transaction(conn, log_buffer, test, c_id, c_w_id, c_d_id, item_number: IntVector, supplier_warehouse: IntVector, quantity: IntVector):
    # 1. Let N denote value of the next available order number D_NEXT_O_ID for district (W_ID,D_ID)
    # 2. Update the district (W ID, D ID) by incrementing D_NEXT_O_ID by one
    N = 0
    with conn.cursor() as cur:
        cur.execute(
            """
            UPDATE 
                district
            SET 
                D_NEXT_O_ID = D_NEXT_O_ID + 1
            WHERE
                (D_W_ID, D_ID) = (%s, %s)
            RETURNING 
                D_NEXT_O_ID - 1;
            """,
            (c_w_id, c_d_id)
        ) 
        
        result = cur.fetchone()
        N = result[0]

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
    item_summaries = []
    for i in range(0, len(item_number)):
        # (a) Check stock quantity for the current item
        S_QUANTITY = 0
        ADJUSTED_QTY = 0
        S_REMOTE_CNT = 0
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                    S_QUANTITY
                FROM 
                    stock
                WHERE
                    S_W_ID = %s
                    AND S_I_ID = %s
                FOR UPDATE;
                """,
                (supplier_warehouse[i], item_number[i]),
            ) # uses primary key index

            result = cur.fetchone()
            S_QUANTITY = result[0]
        
            # (b) Calculate adjusted quantity
            ADJUSTED_QTY = S_QUANTITY - quantity[i]

            # (c) If adjusted quantity < 10, set adjusted quantity += 100
            if ADJUSTED_QTY < 10:
                ADJUSTED_QTY += 100

            # (d) Update the stock for the item and warehouse
            if supplier_warehouse[i] != c_w_id:
                S_REMOTE_CNT = 1

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
            ) # uses primary key index


        # (e) Calculate ITEM_AMOUNT (extract I_NAME also, because you need it in the output)
        ITEM_AMOUNT = 0
        I_NAME = ''
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    I_PRICE, I_NAME
                FROM 
                    item
                WHERE
                    I_ID = %s;
                """,
                (item_number[i],),
            ) # uses primary key index

            result = cur.fetchone()
            I_PRICE = result[0]
            I_NAME = result[1]
            ITEM_AMOUNT = quantity[i] * I_PRICE

        # (f) Update TOTAL_AMOUNT
        TOTAL_AMOUNT += ITEM_AMOUNT

        # (g) Create a new order line
        OL_DIST_INFO = ""
        with conn.cursor() as cur:
            cur.execute(
                sql.SQL(
                """
                SELECT {district_info} FROM stock WHERE S_W_ID = %s AND S_I_ID = %s;
                """
                ).format(
                    district_info=sql.Identifier(district_id_to_string(c_d_id).lower()) # cockroachdb stores column names in lowercase
                ),
                (supplier_warehouse[i], item_number[i]),
            ) # uses primary key index
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

        # Extra step: Record down the I_NAME, OL_AMOUNT and S_QUANTITY (which is the ADJUSTED_QTY) for reporting at the end
        item_summaries.append(ItemSummary(I_NAME, ITEM_AMOUNT, ADJUSTED_QTY))

    
    # 6. Calculate the total value of this transaction
    W_TAX = 0
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT W_TAX FROM warehouse WHERE W_ID = %s;
            """,
            (c_w_id,),
        )
        result = cur.fetchone()
        W_TAX = result[0]

    D_TAX = 0
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT 
                D_TAX 
            FROM
                district 
            WHERE
                (D_W_ID, D_ID) = (%s, %s);
            """,
            (c_w_id, c_d_id),
        )
        result = cur.fetchone()
        D_TAX = result[0]

    
    C_DISCOUNT = 0
    result = []
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT
                C_W_ID, C_D_ID, C_ID, C_LAST, C_CREDIT, C_DISCOUNT
            FROM
                customer
            WHERE 
                (C_W_ID, C_D_ID, C_ID) = (%s, %s, %s);
            """,
            (c_w_id, c_d_id, c_id),
        )
        result = cur.fetchone()
        C_DISCOUNT = result[5]
    
    TOTAL_AMOUNT = TOTAL_AMOUNT * (1 + D_TAX + W_TAX) * (1 - C_DISCOUNT)
    
    # Generate the output
    log_buffer.append("Output for New Order Transaction")

    with conn.cursor() as cur:
        # Customer identifier
        log_buffer.append(f"Customer identifier: {result}")

        # Warehouse and district tax
        log_buffer.append(f"W_TAX:{W_TAX}, D_TAX:{D_TAX}")

        # Order number and entry date
        cur.execute(
            """
            SELECT 
                O_ENTRY_D
            FROM 
                "order"
            WHERE
                (O_W_ID, O_D_ID, O_ID) = (%s, %s, %s);
            """,
            (c_w_id, c_d_id, N),
        )
        result = cur.fetchone()
        O_ENTRY_D = result[0]
        log_buffer.append(f"O_ID: {N}, O_ENTRY_D: {O_ENTRY_D}")

        # Number of items and total amount
        log_buffer.append(f"NUM_ITEMS: {len(item_number)}, TOTAL_AMOUNT: {TOTAL_AMOUNT}")

        # Output summary of each item
        for i in range(len(item_number)):
            log_buffer.append(f"Item {i + 1}:")
            log_buffer.append(f"ITEM_NUMBER: {item_number[i]}")
            log_buffer.append(f"I_NAME: {item_summaries[i].name}")
            log_buffer.append(f"SUPPLIER_WAREHOUSE: {supplier_warehouse[i]}")
            log_buffer.append(f"QUANTITY: {quantity[i]}")
            log_buffer.append(f"OL_AMOUNT: {item_summaries[i].ol_amount}")
            log_buffer.append(f"S_QUANTITY: {item_summaries[i].s_quantity}")
        
        log_buffer.append("End of output for New Order Transaction")
    conn.commit()
    logging.debug("new order finished")
    
    

def district_id_to_string(id: int):
    """
    Takes id and returns "S_DIST_id", zero-padded to two places (e.g 3 -> S_DIST_03, 10 -> S_DIST_10).
    """
    if id < 10:
        return "S_DIST_0" + str(id)
    else:
        return "S_DIST_10"

class ItemSummary:
    """
    Remember the I_NAME, OL_AMOUNT and S_QUANTITY for the report
    """
    def __init__(self, name, ol_amount, s_quantity):
        self.name = name
        self.ol_amount = ol_amount
        self.s_quantity = s_quantity
