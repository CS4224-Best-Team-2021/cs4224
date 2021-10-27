import logging

IntVector = list[int]

def new_order_transaction(conn, c_w_id, c_d_id, c_id, item_numbers: IntVector, supplier_warehouses: IntVector, quantities: IntVector):
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
            UPDATE district
            SET
            """
        )
    # 3. Create a new order

    # 4. Initialise total amount to 0

    # 5. For each item, update quantity

    # 6. Calculate the total value of this transaction
    pass