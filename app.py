from flask import Flask, url_for, json, Response, request, jsonify
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
    order_info = db.insertAndLeaveOpen('INSERT INTO ORDERS (orders.Customer_ID, DateTime, Status) VALUES (%s, LOCALTIME(),%s)', [customer_id, 0])

    # Get the Order_ID from the database
    # db = MySQL_Database()
    # order_ID_list =  db.query('SELECT Order_ID FROM orders WHERE Customer_ID = (%s) ORDER BY orders.DateTime', [customer_id])
    # order_ID_var = order_ID_list[0]["Order_ID"]
    # print(order_ID_var)

    # Create an Order_Details entry in the database
    for item in order_details_list:
        order_details = db.insertAndLeaveOpen('INSERT INTO order_details (Order_ID) SELECT Order_ID FROM orders WHERE Customer_ID = (%s) ORDER BY DateTime DESC LIMIT 1', [customer_id])

        # Get the Order_Details_ID from the database
        # db = MySQL_Database()
        # order_Details_ID_list = db.query('SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = %s', [order_ID_var])
        # order_Details_ID_var = order_Details_ID_list[0]["MAX(Order_Details_ID)"];

        # Create an Item_Details entry in the database
        for ingredient in item:
            item_details = db.insertAndLeaveOpen('INSERT INTO item_details (Order_Details_ID, Stock_ID) VALUES ((SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = (SELECT Order_ID FROM orders WHERE Customer_ID = (%s) ORDER BY DateTime DESC LIMIT 1)), %s)', [customer_id, ingredient])

            updateIngredients = db.insertAndLeaveOpen('UPDATE stock SET Stock_Level = Stock_Level-1 where Stock_ID = %s', [ingredient])
            if updateIngredients is None:
                updateStatus = db.insertAndLeaveOpen('DELETE FROM orders WHERE Order_ID = (SELECT o.Order_ID FROM (SELECT * FROM orders) AS o WHERE Customer_ID = %s ORDER BY DateTime DESC LIMIT 1)', [customer_id])
                return Response(json.dumps({"Insufficient Ingredients": ingredient}))

    db.check_and_close_connection()

    return Response(json.dumps({"Order": "Added"}))

@app.route('/ingredients/all', methods=["GET"])
def allIngredients():
    # Setup database connection
    db = MySQL_Database()

    #Gets list of all stock in the database
    stock_information = db.query('SELECT * FROM stock', [])
    if len(stock_information) > 0:
        for key, value in stock_information[0].items():
            if value is None:
                stock_information[0][key] = ""
        return Response(json.dumps(stock_information))
    else:
        return Response(json.dumps({"Stock": "void"}))

@app.route('/ingredients/available', methods=["GET"])
def availableIngredients():
    # Setup database connection
    db = MySQL_Database()

    #Gets list of all available stock in the database
    stock_information = db.query('SELECT * FROM stock WHERE Stock_Level > 0', [])
    if len(stock_information) > 0:
        for key, value in stock_information[0].items():
            if value is None:
                stock_information[0][key] = ""
        return Response(json.dumps(stock_information))
    else:
        return Response(json.dumps({"Stock": "void"}))

@app.route('/ingredients/<stock_name>', methods=["GET"])
def ingredientByName(stock_name):
    # Setup database connection
    db = MySQL_Database()

    #Gets list of all available stock in the database
    stock_information = db.query('SELECT * FROM stock WHERE Ingredient_Name = %s', [stock_name])
    if len(stock_information) > 0:
        for key, value in stock_information[0].items():
            if value is None:
                stock_information[0][key] = ""
        return Response(json.dumps(stock_information))
    else:
        return Response(json.dumps({"Stock": "void"}))

@app.route('/ingredients/<int:stock_id>', methods=["GET"])
def ingredientByID(stock_id):
    # Setup database connection
    db = MySQL_Database()

    #Gets list of all available stock in the database
    stock_information = db.query('SELECT * FROM stock WHERE Stock_ID = %s', [stock_id])
    if len(stock_information) > 0:
        for key, value in stock_information[0].items():
            if value is None:
                stock_information[0][key] = ""
        return Response(json.dumps(stock_information))
    else:
        return Response(json.dumps({"Stock": "void"}))

@app.route('/order/<int:order_id>', methods=["GET"])
def orderById(order_id):
    # Setup database connection
    db = MySQL_Database()

    # Gets the details of an order from a given order id
    order_details = db.query('SELECT o.Order_ID, o.Customer_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE o.Order_ID = %s AND od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID', [order_id])

    metadata = {}

    for key in order_details[0]:
        metadata[key] = order_details[0][key]

    print(metadata)

    jsondict = {"order_details_list": metadata}
    stockdetails = {}

    prev = -1
    for x in order_details:
        itemNumber = x['Order_Details_ID']
        if itemNumber != prev:

            stockdetails[str(itemNumber)] = []
            stockdetails[str(itemNumber)].append(x['Stock_ID'])
            prev = itemNumber
        else:
            stockdetails[str(itemNumber)].append(x['Stock_ID'])

    jsondict["item_details_list"] = stockdetails

    return Response(json.dumps(jsondict))

@app.route('/order/list/<int:user_id>', methods=["GET"])
def orderByCustomer(user_id):
    # Setup database connection
    db = MySQL_Database()

    uberlist = []

    # Gets the details of an order from a given order id
    order_details = db.query(
        'SELECT o.Order_ID, o.Customer_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE o.Customer_ID = %s AND od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID',
        [user_id])

    if order_details:
        order_id = -1

        for ingredient in order_details:

            if ingredient["Order_ID"] != order_id:
                if order_id != -1:
                    print("Appending order")
                    uberlist.append(jsondict)

                order_id = ingredient["Order_ID"]

                metadata = {}

                for key in ingredient:
                    metadata[key] = ingredient[key]

                print(metadata)

                jsondict = {"order_details_list": metadata}
                stockdetails = {}

                itemNumber = ingredient['Order_Details_ID']
                stockdetails[str(itemNumber)] = []
                stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                prev = itemNumber

            else:
                itemNumber = ingredient['Order_Details_ID']
                if itemNumber != prev:
                    jsondict["item_details_list"] = stockdetails
                    stockdetails[str(itemNumber)] = []
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                    prev = itemNumber
                else:
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])

        jsondict["item_details_list"] = stockdetails
        uberlist.append(jsondict)

        return Response(json.dumps(uberlist))

    else:
        return Response(json.dumps({'order_details_list': 'None'}))

@app.route('/customer/add', methods=["POST"])
def addCustomer():
    json = request.get_json(silent=True)
    print(json)

    username = json['Username']

    return Response(json.dumps({'username' : username}))

if __name__ == '__main__':
    app.run()