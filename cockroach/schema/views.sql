USE wholesaledb;

-- VIEWS

/*
CREATE MATERIALIZED VIEW top_balance
AS 
SELECT 
    c.C_FIRST,
    c.C_MIDDLE,
    c.C_LAST,
    c.C_BALANCE,
    (SELECT W_NAME FROM Warehouse AS w WHERE w.W_ID = c.C_W_ID) AS Warehouse_Name,
    (SELECT D_NAME FROM District AS d WHERE d.D_ID = c.C_D_ID AND d.D_W_ID = c.C_W_ID) AS District_Name
FROM 
    Customer AS c
ORDER BY
    c.C_BALANCE DESC
LIMIT 10;

CREATE MATERIALIZED VIEW related_customer_view
AS
SELECT DISTINCT
    c1.C_W_ID AS C_W_ID1, 
    c1.C_D_ID AS C_D_ID1, 
    c1.C_ID AS C_ID1, 
    c2.C_W_ID AS C_W_ID2, 
    c2.C_D_ID AS C_D_ID2, 
    c2.C_ID AS C_ID2
FROM
    customer AS c1,
    customer AS c2,
    "order" AS o1,
    "order" AS o2,
    order_line AS ol1,
    order_line AS ol2,
    order_line AS ol3,
    order_line AS ol4
WHERE 
    -- c1 and c2 in different warehouses
    c1.C_W_ID != c2.C_W_ID
    -- c1 has o1
    AND c1.C_W_ID = o1.O_W_ID
    AND c1.C_D_ID = o1.O_D_ID
    AND c1.C_ID = o1.O_C_ID
    -- c2 has o2
    AND c2.C_W_ID = o2.O_W_ID
    AND c2.C_D_ID = o2.O_D_ID
    AND c2.C_ID = o2.O_C_ID
    -- ol1 in o1
    AND  ol1.OL_W_ID = o1.O_W_ID
    AND  ol1.OL_D_ID = o1.O_D_ID
    AND  ol1.OL_O_ID = o1.O_ID
    -- OL1 and OL2 are in o1
    AND ol1.OL_W_ID = ol2.OL_W_ID 
    AND ol1.OL_D_ID = ol2.OL_D_ID
    AND ol1.OL_O_ID = ol2.OL_O_ID
    -- OL3 and OL4 are in the same order
    AND ol3.OL_W_ID = ol4.OL_W_ID
    AND ol3.OL_D_ID = ol4.OL_D_ID
    AND ol3.OL_O_ID = ol4.OL_O_ID
    -- ol3 and ol4 are in o2
    AND  ol3.OL_W_ID = o2.O_W_ID
    AND  ol3.OL_D_ID = o2.O_D_ID
    AND  ol3.OL_O_ID = o2.O_ID
    -- OL1 and OL2 are not the same items
    AND ol1.OL_I_ID != ol2.OL_I_ID 
    -- OL3 and OL4 are not the same items
    AND ol3.OL_I_ID != ol4.OL_I_ID 
    -- OL1 and OL3 are the same items
    AND ol1.OL_I_ID = ol3.OL_I_ID 
    -- OL2 and OL4 are the same items
    AND ol2.OL_I_ID = ol4.OL_I_ID;
*/
