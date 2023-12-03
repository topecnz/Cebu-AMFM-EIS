CREATE DATABASE amfm-eis;

-- select database.
USE amfm-eis;

CREATE TABLE employee(
    emp_id INT NOT NULL AUTO_INCREMENT,
    emp_fname varchar(1024) NOT NULL,
    emp_mname varchar(1024),
    emp_lname varchar(1024) NOT NULL,
    emp_birthdate date NOT NULL,
    emp_phone varchar(12) NOT NULL,
    emp_email varchar(1024) NOT NULL,
    emp_address varchar(1024) NOT NULL,
    emp_created_at TIMESTAMP DEFAULT NOW(),
    emp_updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (emp_id)
);
CREATE TABLE customer(
    cus_id INT NOT NULL AUTO_INCREMENT,
    cus_fname varchar(1024) NOT NULL,
    cus_mname varchar(1024),
    cus_lname varchar(1024) NOT NULL,
    cus_phone varchar(12) NOT NULL,
    cus_created_at TIMESTAMP DEFAULT NOW(),
    cus_updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (cus_id)
);
CREATE TABLE supplier(
    sup_id INT NOT NULL,
    sup_name varchar(1024) NOT NULL,
    sup_phone varchar(12) NOT NULL,
    sup_email varchar(1024) NOT NULL,
    sup_created_at TIMESTAMP DEFAULT NOW(),
    sup_updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (sup_id)
);
CREATE TABLE account_type(
    acc_type_id INT NOT NULL,
    acc_type_name varchar(64) NOT NULL,
    PRIMARY KEY (acc_type_id)
);
CREATE TABLE account(
    acc_id INT NOT NULL AUTO_INCREMENT,
    acc_username varchar(32) NOT NULL UNIQUE,
    acc_password varchar(32) NOT NULL,
    acc_type_id INT NOT NULL,
    emp_id INT NOT NULL,
    PRIMARY KEY (acc_id),
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
    FOREIGN KEY (acc_type_id) REFERENCES account_type(acc_type_id)
);
CREATE TABLE product_type(
    prod_type_id INT NOT NULL,
    prod_type_name varchar(1024) NOT NULL,
    PRIMARY KEY (prod_type_id)
);
CREATE TABLE product_brand(
    prod_br_id INT NOT NULL,
    prod_br_name varchar(1024) NOT NULL,
    PRIMARY KEY (prod_br_id)
);
CREATE TABLE product(
    prod_id INT NOT NULL AUTO_INCREMENT,
    prod_name varchar(1024) NOT NULL,
    prod_desc varchar(1024),
    prod_price FLOAT default 0.0,
    prod_created_at TIMESTAMP DEFAULT NOW(),
    prod_updated_at TIMESTAMP DEFAULT NOW(),
    prod_type_id INT NOT NULL,
    PRIMARY KEY (prod_id),
    FOREIGN KEY (prod_type_id) REFERENCES product_type(prod_type_id)
);
CREATE TABLE inventory(
    in_id INT NOT NULL,
    in_qty INT DEFAULT 0,
    int_status enum('Available', 'Not Available') default 'Available',
    in_created_at TIMESTAMP DEFAULT NOW(),
    in_updated_at TIMESTAMP DEFAULT NOW(),
    prod_id INT NOT NULL,
    PRIMARY KEY (in_id),
    FOREIGN KEY (prod_id) REFERENCES product(prod_id)
);
CREATE TABLE supplier_item(
    sup_itm_id INT NOT NULL,
    sup_itm_qty INT DEFAULT 0,
    sup_itm_dr varchar(1024) NOT NULL,
    sup_itm_status enum('Delivered', 'Pending') DEFAULT 'Pending',
    sup_itm_created_at TIMESTAMP DEFAULT NOW(),
    sup_itm_updated_at TIMESTAMP DEFAULT NOW(),
    prod_id INT NOT NULL,
    PRIMARY KEY (sup_itm_id),
    FOREIGN KEY (prod_id) REFERENCES product(prod_id)
);
CREATE TABLE invoice(
    inv_id INT NOT NULL AUTO_INCREMENT,
    inv_date TIMESTAMP DEFAULT NOW(),
    inv_amount FLOAT DEFAULT 0.0,
    cus_id INT,
    emp_id INT NOT NULL,
    PRIMARY KEY (inv_id),
    FOREIGN KEY (cus_id) REFERENCES customer(cus_id),
    FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
);
CREATE TABLE order_list(
    ord_id INT NOT NULL AUTO_INCREMENT,
    ord_price FLOAT default 0.0,
    ord_qty INT default 0,
    prod_id INT NOT NULL,
    inv_id INT NOT NULL ,
    PRIMARY KEY (ord_id),
    FOREIGN KEY (prod_id) REFERENCES product(prod_id),
    FOREIGN KEY (inv_id) REFERENCES invoice(inv_id)
);

-- -- might be optional or it depends to the client if they need to have history to check their activities.
-- CREATE TABLE history(
--     his_id INT NOT NULL AUTO_INCREMENT,
--     PRIMARY KEY (his_id)
-- );

-- -- trying to import via third-party api.
-- CREATE TABLE province(
--     prv_id INT NOT NULL AUTO_INCREMENT,
--     PRIMARY KEY (prv_id)
-- );
-- CREATE TABLE city(
--     cit_id INT NOT NULL AUTO_INCREMENT,
--     PRIMARY KEY (cit_id)
-- );
-- CREATE TABLE barangay(
--     bar_id INT NOT NULL AUTO_INCREMENT,
--     PRIMARY KEY (brg_id)
-- );


DROP TABLE account_type;
DROP TABLE product_type;
DROP TABLE product_brand;
DROP TABLE employee;
DROP TABLE customer;
DROP TABLE supplier;
DROP TABLE account;
DROP TABLE product;
DROP TABLE inventory;
DROP TABLE supplier_item;
DROP TABLE order_list;
DROP TABLE invoice;


account_type product_type product_brand employee customer supplier account product inventory supplier_item order_list invoice