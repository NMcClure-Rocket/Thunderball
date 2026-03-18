//USER12A JOB ,CLASS=A,MSGCLASS=X,REGION=0M,
//  NOTIFY=&SYSUID
//* *------------------------------------------------------------------*
//*
//STEP0020 EXEC PGM=IKJEFT01,DYNAMNBR=20
//STEPLIB  DD   DISP=SHR,DSN=HL2D.SDSNEXIT
//         DD   DISP=SHR,DSN=DSN.VD10.SDSNLOAD
//         DD   DISP=SHR,DSN=DSN.VD10.RUNLIB.LOAD
//SYSTSPRT DD  SYSOUT=*
//SYSPRINT DD  SYSOUT=*
//SYSUDUMP DD  SYSOUT=*
//SYSTSIN  DD  *
  DSN SYSTEM(HL2D)
  RUN PROGRAM(DSNTEP2)  PLAN(DSNTEP2) -
       LIB('DSN.VD10.RUNLIB.LOAD')
  END
//SYSIN    DD  *
CREATE DATABASE VILNIUS                        
    STOGROUP SYSDEFLT                         
    BUFFERPOOL BP0                            
    INDEXBP BP0                               
    CCSID EBCDIC;    

CREATE TABLE BASEPRICE (
    PRICEID       INTEGER       NOT NULL,
    NAME          VARCHAR(100),
    PRICE         DECIMAL(10,2),
    IMAGELINK     VARCHAR(255),
    PRIMARY KEY (PRICEID)
)
IN DATABASE VILNIUS;

CREATE TABLE INVENTORY (                       
    ITEMID        INTEGER       NOT NULL,      
    NAME          VARCHAR(100),                
    DESCRIPTION   VARCHAR(255),                
    FORMAT        VARCHAR(50),                 
    POTENCY       INTEGER,                     
    REUSABLE      CHAR(1),                     
    CATEGORY      VARCHAR(50),                 
    PRICE         DECIMAL(10,2),               
    AMOUNT        INTEGER,    
    BASEINFO      INTEGER,                 
    PRIMARY KEY (ITEMID),
    FOREIGN KEY (BASEINFO)
        REFERENCES BASEPRICE (PRICEID)
)                                              
IN DATABASE VILNIUS;                             

CREATE TABLE CUSTOMER (                        
    CUSTOMERID    INTEGER       NOT NULL,      
    FIRST_NAME    VARCHAR(100),         
    LAST_NAME     VARCHAR(100),          
    EMAIL         VARCHAR(150),                
    PASSWORD      VARCHAR(200),                
    PRIMARY KEY (CUSTOMERID)                   
)                                              
IN DATABASE VILNIUS;                             

CREATE TABLE CCI (                             
    CCID           INTEGER       NOT NULL,     
    NUMBER         BIGINT,                     
    SECURITY_CODE  SMALLINT,                   
    EXPIRATION     VARCHAR(5),                       
    PROCESSOR      VARCHAR(20),      
    FIRST_NAME    VARCHAR(100),         
    LAST_NAME     VARCHAR(100),      
    ADDRESS       VARCHAR(150),                
    ADDR_2        VARCHAR(150),                
    CITY          VARCHAR(100),                
    STATE         CHAR(2),                     
    COUNTRY       VARCHAR(100),                
    ZIP           VARCHAR(20), 
    CUSTOMERID    INTEGER,
    PRIMARY KEY (CCID),
    FOREIGN KEY (CUSTOMERID)
        REFERENCES CUSTOMER (CUSTOMERID)                        
)                                              
IN DATABASE VILNIUS;                             

CREATE TABLE SHIPPINGADDRESS (                  
    ADDRESSID     INTEGER       NOT NULL,      
    FIRST_NAME    VARCHAR(100),         
    LAST_NAME     VARCHAR(100),      
    ADDRESS       VARCHAR(150),                
    ADDR_2        VARCHAR(150),                
    CITY          VARCHAR(100),                
    STATE         CHAR(2),                     
    COUNTRY       VARCHAR(100),                
    ZIP           VARCHAR(20),                 
    CUSTOMERID    INTEGER       NOT NULL,      
    PRIMARY KEY (ADDRESSID),               
    FOREIGN KEY (CUSTOMERID)               
        REFERENCES CUSTOMER (CUSTOMERID)   

)                                              
IN DATABASE VILNIUS;  

CREATE TABLE INVORDER (                        
     ORDERID        INTEGER       NOT NULL,    
     PURCHASE_TIME  TIMESTAMP,                 
     DELIVERY_EST   TIMESTAMP,                 
     ITEMID         INTEGER       NOT NULL,    
     AMOUNT         INTEGER,                   
     TRANSACTION    DECIMAL(10,2),             
     CCID           INTEGER       NOT NULL,    
     CUSTOMERID     INTEGER       NOT NULL,    
     ADDRESSID      INTEGER       NOT NULL,    
     PRIMARY KEY (ORDERID),                    
     FOREIGN KEY (ITEMID)                      
        REFERENCES INVENTORY (ITEMID),        
     FOREIGN KEY (CCID)                        
        REFERENCES CCI (CCID),                
     FOREIGN KEY (CUSTOMERID)                  
        REFERENCES CUSTOMER (CUSTOMERID),     
     FOREIGN KEY (ADDRESSID)                   
        REFERENCES SHIPPINGADDRESS (ADDRESSID) 
)                                             
IN DATABASE VILNIUS;                                                       

   COMMIT; 
