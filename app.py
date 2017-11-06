from flask import Flask, url_for, json, Response
from mysql_db import MySQL_Database
import os
import datetime

app = Flask(__name__)

# Configure application database differently if the application is being run locally
if os.environ['ENV_TYPE'] == 'LOCAL':
    import configparser

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'config.ini')
    config = configparser.ConfigParser()
    config.read(filename)

    local = config['LOCAL']


# API root
@app.route('/')
def api_root():
    data = {'welcome': 'xTreme Burger API'}
    return Response(json.dumps(data))


# Customer database access
# By username
@app.route('/customer/username/<username>', methods=["GET"])
def customer_by_username(username):
    # Setup database connection
    db = MySQL_Database()

    # Query Customer table by username and pull all information if available
    customer_information = db.query('SELECT * FROM customer WHERE customer.Username = %s', [username])
    if len(customer_information) > 0:
        for key, value in customer_information[0].items():
            if value is None:
                customer_information[0][key] = ""
        return Response(json.dumps(customer_information[0]))
    else:
        return Response(json.dumps({"Username": "void"}))


# By email
@app.route('/customer/email/<email>', methods=["GET"])
def customer_by_email(email):
    # Setup database connection
    db = MySQL_Database()

    # Query Customer table by username and pull all information if available
    customer_information = db.query('SELECT * FROM customer WHERE customer.Email = %s', [email])
    if len(customer_information) > 0:
        for key, value in customer_information[0].items():
            if value is None:
                customer_information[0][key] = ""
        return Response(json.dumps(customer_information[0]))
    else:
        return Response(json.dumps({"Username": "void"}))

# By user_id
@app.route('/customer/user_id/<int:user_id>', methods=["GET"])
def customer_by_user_id(user_id):
    # Setup database connection
    db = MySQL_Database()

    # Query customer (by a customer user_id) and pull all information available
    customer_information = db.query('SELECT * FROM customer WHERE customer.Customer_ID = %s', [user_id])
    if len(customer_information) > 0:
        for key, value in customer_information[0].items():
            if value is None:
                customer_information[0][key] = ""
        return Response(json.dumps(customer_information[0]))
    else:
        return Response(json.dumps({"Customer_ID": "void"}))

# Add order
@app.route('/order/add/<int:customer_id>')
def addOrder(customer_id):

    order_details_list = [[11, 41, 51, 61, 81, 101, 111, 141, 191],[341],[371],[411]]

    # Setup database connection
    db = MySQL_Database()

    # Create an Order entry in the database
    order_info = db.insert('INSERT INTO ORDERS (orders.Customer_ID, DateTime, Status) VALUES (%s, NOW(),%s)', [customer_id, 0])

    # Get the Order_ID from the database
    db = MySQL_Database()
    order_ID_list =  db.query('SELECT Order_ID FROM orders WHERE Customer_ID = (%s) ORDER BY orders.DateTime', [customer_id])
    order_ID_var = order_ID_list[0]["Order_ID"]
    print(order_ID_var)

    print(order_details_list)

    # Create an Order_Details entry in the database
    for x in order_details_list:
        print("x")
        print(x)
        db = MySQL_Database()
        order_details = db.insert('INSERT INTO order_details (Order_ID) VALUE (%s)', [order_ID_var])

        # Get the Order_Details_ID from the database
        db = MySQL_Database()
        order_Details_ID_list = db.query('SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = %s', [order_ID_var])
        order_Details_ID_var = order_Details_ID_list[0]["MAX(Order_Details_ID)"];

        # Create an Item_Details entry in the database
        for y in x:
            print("y")
            print(y)
            db = MySQL_Database()
            item_details = db.insert('INSERT INTO item_details (Order_Details_ID, Stock_ID) VALUES (%s, %s)', [order_Details_ID_var, y])

            db = MySQL_Database()
            updateIngredients = db.update('UPDATE stock SET Stock_Level = Stock_Level-1 where Stock_ID = %s', [y])
            if updateIngredients is None:
                db = MySQL_Database()
                updateStatus = db.update('UPDATE orders SET status = 3 WHERE Order_ID = %s', [order_ID_var])
                return Response(json.dumps({"Insufficient Ingredients": y}))

    return Response(json.dumps({"Order": "Added"}))

if __name__ == '__main__':
    app.run()