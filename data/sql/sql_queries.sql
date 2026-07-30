create database sales_analysis;
use sales_analysis;

/* CREATE TABLES AS CUSTOMERS
create table customers(
customer_id INT PRIMARY KEY,
    customer_name VARCHAR(50),
    city VARCHAR(50),
    phone VARCHAR(15)
);

/* INSERT DATA INTO TCUSTOMERS TABLE
INSERT INTO customers VALUES
(1, 'Ravi', 'Hyderabad', '9876543210'),
(2, 'Anil', 'Chennai', '9876543211'),
(3, 'Priya', 'Mumbai', '9876543212'),
(4, 'Sita', 'Delhi', '9876543213'),
(5, 'Kiran', 'Bangalore', '9876543214');

/*CREATE PRODUCTS TABLE

CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(50),
    category VARCHAR(50),
    price DECIMAL(10,2)
);

/*INSERT DATA INTO PRODUCTS TABLE

INSERT INTO products VALUES
(101, 'Laptop', 'Electronics', 60000),
(102, 'Mouse', 'Electronics', 1000),
(103, 'Chair', 'Furniture', 5000),
(104, 'Keyboard', 'Electronics', 2500),
(105, 'Desk', 'Furniture', 8000);

/* CREATE TABLE AS ORDERS

CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    product_id INT,
    quantity INT,
    order_date DATE,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

/* INSERT DATA INTO ORDERS TABLE

INSERT INTO orders VALUES
(1001, 1, 101, 2, '2026-07-01'),
(1002, 2, 102, 5, '2026-07-02'),
(1003, 1, 103, 1, '2026-07-03'),
(1004, 3, 104, 3, '2026-07-04'),
(1005, 4, 105, 2, '2026-07-05'),
(1006, 5, 101, 1, '2026-07-06');

/* CHECK TABLES 

SELECT * FROM customers;

SELECT * FROM products;

SELECT * FROM orders;

/*SELECT

SELECT customer_name, city FROM products;

SELECT customer_name, city from customers;


/* WHERE

SELECT * FROM customers WHERE city = 'Hyderabad';

SELECT * FROM products WHERE price > 5000;

SELECT * FROM orders WHERE quantity > 2;

/*ORDER BY
SELECT * FROM products ORDER BY price ASC;

SELECT * FROM products ORDER BY price DESC;

SELECT * FROM customers ORDER BY customer_name ASC; 

/*DISTINCT

SELECT DISTINCT city FROM customers;

SELECT DISTINCT category FROM products;

/* AGGREGATE FUNCTIONS

SELECT COUNT(*) AS total_customers FROM customers;

SELECT COUNT(*) AS total_products FROM products;

SELECT SUM(quantity) AS total_quantity FROM orders;

SELECT AVG(price) AS average_price FROM products;

SELECT MAX(price) AS highest_price FROM products;

SELECT MIN(price) AS lowest_price FROM products;


/* GROUP BY

SELECT category,COUNT(*) AS product_count FROM products GROUP BY category;

SELECT customer_id,SUM(quantity) AS total_quantity FROM orders GROUP BY customer_id;


/*HAVING

SELECT category,COUNT(*) AS product_count FROM products GROUP BY category HAVING COUNT(*) > 1;

SELECT customer_id,SUM(quantity) AS total_quantity FROM orders GROUP BY customer_id HAVING SUM(quantity) > 2;


/*CALCULATE REVENUE

SELECT
    o.product_id,
    o.quantity,
    o.quantity * p.price AS revenue
FROM orders AS o
JOIN products AS p
    ON o.product_id = p.product_id;
  
  
  /* INNER JOIN
  
    SELECT
    c.customer_name,
    c.city,
    o.order_id,
    o.quantity
FROM customers AS c
INNER JOIN orders AS o
    ON c.customer_id = o.customer_id;
    
    
/*JOIN CUSTOMERS + ORDERS
    
    SELECT
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    o.quantity,
    p.price,
    o.quantity * p.price AS revenue
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN products AS p
    ON o.product_id = p.product_id;
    
    
/* PRODUCT PERFORMANCE

SELECT
    p.product_name,
    SUM(o.quantity) AS total_quantity,
    SUM(o.quantity * p.price) AS total_revenue
FROM products AS p
JOIN orders AS o
    ON p.product_id = o.product_id
GROUP BY p.product_name;


/* CUSTOMER REVENUE

SELECT
    c.customer_name,
    SUM(o.quantity * p.price) AS total_revenue
FROM customers AS c
JOIN orders AS o
    ON c.customer_id = o.customer_id
JOIN products AS p
    ON o.product_id = p.product_id
GROUP BY c.customer_name
ORDER BY total_revenue DESC;


/* SUBQUERY 

SELECT * FROM products WHERE price > (SELECT AVG(price) FROM products);


SELECT * FROM orders WHERE quantity > (SELECT AVG(quantity) FROM orders);


/*EXISTS

SELECT * FROM customers AS c
WHERE EXISTS (
    SELECT 1
    FROM orders AS o
    WHERE o.customer_id = c.customer_id
);


/* CASE

SELECT product_name,price,
    CASE
        WHEN price >= 50000 THEN 'High Price'
        WHEN price >= 5000 THEN 'Medium Price'
        ELSE 'Low Price'
    END AS price_category
FROM products;

/* WINDOW FUNCTION - RANK

SELECT product_name,price,
    RANK() OVER (
        ORDER BY price DESC
    ) AS price_rank
FROM products;

/* WINDOW FUNCTION - ROW NUMBER

SELECT product_name, price,
    ROW_NUMBER() OVER (
        ORDER BY price DESC
    ) AS row_num
FROM products;


/* RUNNING TOTAL

SELECT order_id,order_date,quantity,
    SUM(quantity) OVER (
        ORDER BY order_date
    ) AS running_quantity
FROM orders;

    
    