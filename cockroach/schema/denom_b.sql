USE wholesaledb;

DROP TABLE IF EXISTS denom_order_order_line;
CREATE TABLE denom_order_order_line (
    DOOL_W_ID INT,
    DOOL_D_ID INT,
    DOOL_ID INT,
    DOOL_C_ID INT,
    DOOL_CARRIER_ID INT CHECK (O_CARRIER_ID BETWEEN 0 AND 10),
    DOOL_OL_CNT FLOAT,
    DOOL_ALL_LOCAL FLOAT,
    DOOL_ENTRY_D TIMESTAMP,
    DOOL_NUMBER INT,
    DOOL_I_ID INT REFERENCES item(I_ID),
    DOOL_DELIVERY_D TIMESTAMP,
    DOOL_AMOUNT FLOAT,
    DOOL_SUPPLY_W_ID INT,
    DOOL_QUANTITY FLOAT,
    DOOL_DIST_INFO STRING,
    PRIMARY KEY (DOOL_W_ID, DOOL_D_ID, DOOL_ID),
    INDEX order_dt_index (DOOL_ENTRY_D),
    CONSTRAINT order_customer_fk FOREIGN KEY(DOOL_W_ID, DOOL_D_ID, DOOL_C_ID) REFERENCES customer(C_W_ID, C_D_ID, C_ID),
);

INSERT INTO denom_order_order_line
SELECT 
    o.O_W_ID,
    o.O_D_ID,
    o.O_ID,
    o.O_C_ID,
    o.O_CARRIER_ID,
    o.O_OL_CNT,
    o.O_ALL_LOCAL,
    o.O_ENTRY_D,
    ol.OL_NUMBER,
    ol.OL_I_ID,
    ol.OL_DELIVERY_D,
    ol.OL_AMOUNT,
    ol.OL_SUPPLY_W_ID,
    ol.OL_QUANTITY,
    ol.OL_DIST_INFO
FROM 
    order o INNER JOIN order_line ol
ON 
    o.O_W_ID = ol.OL_W_ID
    AND o.O_D_ID = ol.OL_D_ID
    AND o.O_ID = ol.OL_O_ID;