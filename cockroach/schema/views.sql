USE wholesaledb;

-- VIEWS

CREATE VIEW top_balance
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
