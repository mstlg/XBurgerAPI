INSERT INTO Orders (orders.Customer_ID, DateTime, Status) VALUES (21, NOW(), 0);
SELECT Order_ID FROM orders WHERE Customer_ID = 21 ORDER BY orders.DateTime;

INSERT INTO order_details (Order_ID) VALUE (1);

SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = 1;

SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = 1;

INSERT INTO item_details (Order_Details_ID, Stock_ID) VALUES ((SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = (SELECT Order_ID FROM orders WHERE Customer_ID = (%s) ORDER BY DateTime ASC LIMIT 1)), %s)

SELECT orders.Order_ID, customer.FullName, stock.Ingredient_Name FROM orders JOIN order_details ON orders.Order_ID = order_details.Order_ID JOIN item_details ON order_details.Order_Details_ID = item_details.Order_Details_ID JOIN stock ON item_details.Stock_ID = stock.Stock_ID JOIN customer ON orders.Customer_ID = customer.Customer_ID WHERE orders.Customer_ID = 1

SELECT customer.FullName, stock.Ingredient_Name FROM orders JOIN order_details ON orders.Order_ID = order_details.Order_ID JOIN item_details ON order_details.Order_Details_ID = item_details.Order_Details_ID JOIN customer ON orders.Customer_ID = customer.Customer_ID WHERE orders.order_ID = 1

SELECT o.Order_ID, o.Customer_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE o.Order_ID = 11 AND od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID;