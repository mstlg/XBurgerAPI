INSERT INTO Orders (orders.Customer_ID, DateTime, Status) VALUES (21, NOW(), 0);
SELECT Order_ID FROM orders WHERE Customer_ID = 21 ORDER BY orders.DateTime;

INSERT INTO order_details (Order_ID) VALUE (1);

SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = 1;

SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = 1;