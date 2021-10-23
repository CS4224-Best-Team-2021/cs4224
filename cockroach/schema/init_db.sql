DROP DATABASE IF EXISTS wholesaledb;
CREATE DATABASE wholesaledb; 

USE wholesaledb;

DROP TABLE IF EXISTS warehouse;
CREATE TABLE warehouse(
    W_ID INT PRIMARY KEY,
    W_NAME STRING NOT NULL,
    W_STREET_1 STRING NOT NULL,
    W_STREET_2 STRING NOT NULL,
    W_CITY STRING NOT NULL,
    W_STATE STRING NOT NULL,
    W_ZIP STRING NOT NULL,
    W_TAX FLOAT NOT NULL,
    W_YTD FLOAT NOT NULL,
    FAMILY warehouse_w(W_ID, W_YTD),
    FAMILY warehouse_r(W_NAME, W_STREET_1, W_STREET_2, W_CITY, W_STATE, W_ZIP, W_TAX)
);

DROP TABLE IF EXISTS district;
CREATE TABLE district(
    D_W_ID INT REFERENCES warehouse (W_ID),
    D_ID INT,
    D_NAME STRING NOT NULL,
    D_STREET_1 STRING NOT NULL,
    D_STREET_2 STRING NOT NULL,
    D_CITY STRING NOT NULL,
    D_STATE STRING NOT NULL,
    D_ZIP STRING NOT NULL,
    D_TAX FLOAT NOT NULL,
    D_YTD FLOAT NOT NULL,
    D_NEXT_O_ID INT,
    PRIMARY KEY (D_W_ID, D_ID),
    FAMILY district_w(D_NEXT_O_ID, D_YTD, D_W_ID, D_ID),
    FAMILY district_r(D_NAME, D_STREET_1, D_STREET_2, D_CITY, D_STATE, D_ZIP, D_TAX)
);

DROP TABLE IF EXISTS customer;
CREATE TABLE customer(
    C_W_ID INT,
    C_D_ID INT,
    C_ID INT,
    C_FIRST STRING NOT NULL,
    C_MIDDLE STRING,
    C_LAST STRING,
    C_STREET_1 STRING NOT NULL,
    C_STREET_2 STRING NOT NULL,
    C_CITY STRING NOT NULL,
    C_STATE STRING NOT NULL,
    C_ZIP STRING NOT NULL,
    C_PHONE STRING NOT NULL,
    C_SINCE TIMESTAMP NOT NULL,
    C_CREDIT STRING NOT NULL,
    C_CREDIT_LIM FLOAT NOT NULL,
    C_DISCOUNT FLOAT,
    C_BALANCE FLOAT,
    C_YTD_PAYMENT FLOAT,
    C_PAYMENT_CNT INT,
    C_DELIVERY_CNT INT,
    C_DATA STRING,
    PRIMARY KEY (C_W_ID, C_D_ID, C_ID),
    CONSTRAINT customer_district_fk FOREIGN KEY (C_W_ID, C_D_ID) REFERENCES district (D_W_ID, D_ID),
    FAMILY customer_w(C_W_ID, C_D_ID, C_ID, C_BALANCE, C_YTD_PAYMENT, C_PAYMENT_CNT, C_DELIVERY_CNT),
    FAMILY customer_r(C_FIRST, C_MIDDLE, C_LAST, C_STREET_1, C_STREET_2, C_CITY, C_STATE, C_ZIP, C_PHONE, C_SINCE, C_CREDIT, C_CREDIT_LIM, C_DISCOUNT, C_DATA)
);

DROP TABLE IF EXISTS "order";
CREATE TABLE "order"(
    O_W_ID INT,
    O_D_ID INT,
    O_ID INT,
    O_C_ID INT,
    O_CARRIER_ID INT CHECK (O_CARRIER_ID BETWEEN 0 AND 10),
    O_OL_CNT FLOAT,
    O_ALL_LOCAL FLOAT,
    O_ENTRY_D TIMESTAMP,
    PRIMARY KEY (O_W_ID, O_D_ID, O_ID),
    CONSTRAINT order_customer_fk FOREIGN KEY(O_W_ID, O_D_ID, O_C_ID) REFERENCES customer(C_W_ID, C_D_ID, C_ID),
    FAMILY order_w(O_CARRIER_ID, O_ALL_LOCAL),
    FAMILY order_r(O_W_ID, O_D_ID, O_ID, O_ENTRY_D, O_OL_CNT, O_C_ID)
);

DROP TABLE IF EXISTS item;
CREATE TABLE item(
    I_ID INT PRIMARY KEY,
    I_NAME STRING,
    I_PRICE FLOAT,
    I_IM_ID INT,
    I_DATA STRING
);

DROP TABLE IF EXISTS order_line;
CREATE TABLE order_line(
    OL_W_ID INT,
    OL_D_ID INT,
    OL_O_ID INT,
    OL_NUMBER INT,
    OL_I_ID INT REFERENCES item(I_ID),
    OL_DELIVERY_D TIMESTAMP,
    OL_AMOUNT FLOAT,
    OL_SUPPLY_W_ID INT,
    OL_QUANTITY FLOAT,
    OL_DIST_INFO STRING,
    PRIMARY KEY (OL_O_ID, OL_W_ID, OL_D_ID, OL_NUMBER),
    CONSTRAINT orderline_order_fk FOREIGN KEY(OL_W_ID, OL_D_ID, OL_O_ID) REFERENCES "order"(O_W_ID, O_D_ID, O_ID),
    FAMILY order_line_w(OL_DELIVERY_D, OL_W_ID, OL_D_ID, OL_O_ID, OL_NUMBER),
    FAMILY order_line_r(OL_I_ID, OL_AMOUNT, OL_SUPPLY_W_ID, OL_QUANTITY, OL_DIST_INFO) 
);

DROP TABLE IF EXISTS stock;
CREATE TABLE stock(
    S_W_ID INT REFERENCES warehouse(W_ID),
    S_I_ID INT REFERENCES item(I_ID),
    S_QUANTITY FLOAT,
    S_YTD FLOAT,
    S_ORDER_CNT INT,
    S_REMOTE_CNT INT,
    S_DIST_01 STRING,
    S_DIST_02 STRING,
    S_DIST_03 STRING,
    S_DIST_04 STRING,
    S_DIST_05 STRING,
    S_DIST_06 STRING,
    S_DIST_07 STRING,
    S_DIST_08 STRING,
    S_DIST_09 STRING,
    S_DIST_10 STRING,
    S_DATA STRING,
    PRIMARY KEY (S_I_ID, S_W_ID),
    FAMILY stock_w(S_W_ID, S_I_ID, S_QUANTITY, S_YTD, S_ORDER_CNT, S_REMOTE_CNT),
    FAMILY stock_r(S_DIST_01, S_DIST_02, S_DIST_03, S_DIST_04, S_DIST_05, S_DIST_06, S_DIST_07, S_DIST_08, S_DIST_09, S_DIST_10, S_DATA)
);

-- VIEWS

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
