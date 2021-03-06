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
# By username - java access provided
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


# By email - java access provided
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


# Java access provided
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

# Java access provided
@app.route('/order/add/<int:customer_id>', methods=["POST"])
def addOrder(customer_id):

    print("test")

    order_json = request.get_json(silent=True)

    order_details_list = order_json["item_details_list"]

    # Setup database connection
    db = MySQL_Database()

    # Create an Order entry in the database
    order_info = db.insertAndLeaveOpen('INSERT INTO ORDERS (orders.Customer_ID, DateTime, Status) VALUES (%s, LOCALTIME(),%s)', [customer_id, 0])


    # Create an Order_Details entry in the database
    for item in order_details_list:
        order_details = db.insertAndLeaveOpen('INSERT INTO order_details (Order_ID) SELECT Order_ID FROM orders WHERE Customer_ID = (%s) ORDER BY DateTime DESC LIMIT 1', [customer_id])

        # Create an Item_Details entry in the database
        for ingredient in item:
            item_details = db.insertAndLeaveOpen('INSERT INTO item_details (Order_Details_ID, Stock_ID) VALUES ((SELECT MAX(Order_Details_ID) FROM order_details WHERE Order_ID = (SELECT Order_ID FROM orders WHERE Customer_ID = (%s) ORDER BY DateTime DESC LIMIT 1)), %s)', [customer_id, ingredient])

            updateIngredients = db.insertAndLeaveOpen('UPDATE stock SET Stock_Level = Stock_Level-1 where Stock_ID = %s', [ingredient])
            if updateIngredients is None:
                updateStatus = db.insertAndLeaveOpen('DELETE FROM orders WHERE Order_ID = (SELECT o.Order_ID FROM (SELECT * FROM orders) AS o WHERE Customer_ID = %s ORDER BY DateTime DESC LIMIT 1)', [customer_id])
                return Response(json.dumps({"Insufficient Ingredients": ingredient}))

    db.check_and_close_connection()

    return Response(json.dumps({"Order": "Added"}))

# Java access provided
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

# Java access provided
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

@app.route('/ingredients/pending_restock', methods=["GET"])
def lowIngredients():
    # Setup database connection
    db = MySQL_Database()

    # Gets list of all stock in the database
    stock_information = db.query('SELECT * FROM stock WHERE Stock_Level <= 5', [])
    if stock_information:
        for key, value in stock_information[0].items():
            if value is None:
                stock_information[0][key] = ""
        return Response(json.dumps(stock_information))
    else:
        return Response(json.dumps({"Stock": "void"}))

# Java access provided
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

# Java access provided
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

# Java access provided
@app.route('/order/<int:order_id>', methods=["GET"])
def orderById(order_id):
    # Setup database connection
    db = MySQL_Database()

    # Gets the details of an order from a given order id
    order_details = db.query('SELECT o.Order_ID, o.Customer_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE o.Order_ID = %s AND od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID', [order_id])

    metadata = {}

    print(order_details)

    if order_details:

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
    else:
        return Response(json.dumps({'item_details_list': 'no_order'}))


# Java access TO DO
@app.route('/order/list/customer/<int:user_id>', methods=["GET"])
def orderByCustomer(user_id):
    # Setup database connection
    db = MySQL_Database()

    order_list = []

    # Gets the details of an order from a given order id
    order_details = db.query(
        'SELECT o.Order_ID, o.Customer_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE o.Customer_ID = %s AND od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID',
        [user_id])

    if order_details:

        # Initialise order_id to -1 to symbolise that this is the first order being processed
        order_id = -1

        # Loop through each ingredient row in the query result
        for ingredient in order_details:

            # If the order_id is not equal to the previous, then do the following
            if ingredient["Order_ID"] != order_id:
                # If the order is not the first one being processed, this is a new order, we need to append the previous order to the 'uberlist'
                if order_id != -1:
                    print("Appending order")
                    # Append the items_list to the order object
                    order_individual["item_details_list"] = stockdetails
                    # Append the order object to the orders_list
                    order_list.append(order_individual)

                # After processing the previous order (if required), we process the metadata for the current row
                order_id = ingredient["Order_ID"]
                metadata = {}
                for key in ingredient:
                    metadata[key] = ingredient[key]

                # Assign the order metadata to the 'order_details_list' json tag
                order_individual = {"order_details_list": metadata}

                # Initialise the ingredients list for this order_item
                stockdetails = {}
                # Get the item_id for this ingredient and setup
                itemNumber = ingredient['Order_Details_ID']
                # Create a dictionary entry for this item_id which is a blank array
                stockdetails[str(itemNumber)] = []
                # Append the first ingredient to the item_id entry
                stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                # Set the previous item_id to be the current item so that subsequent ingredients are added to the correct item
                prev = itemNumber

            # If the order is equal to the previous, this ingredient forms part of the same order
            else:
                # Get the item_id to check whether the ingredient is part of the same item
                itemNumber = ingredient['Order_Details_ID']
                # If the ingredient is not part of the current item
                if itemNumber != prev:
                    # Add the ingredient to a new item
                    stockdetails[str(itemNumber)] = []
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                    # Set the previous item_id to be the current item so that subsequent ingredients are added to the correct item
                    prev = itemNumber
                # If the ingredient is part of the current item, append it to the list of stock details for that item
                else:
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])

        # Once the loop is completed, finish off the final order to be added
        order_individual["item_details_list"] = stockdetails
        order_list.append(order_individual)

        return Response(json.dumps(order_list))

    else:
        return Response(json.dumps({'order_details_list': 'None'}))


# Java access TO DO
@app.route('/order/list/staff/<int:staff_id>', methods=["GET"])
def orderByStaff(staff_id):
    # Setup database connection
    db = MySQL_Database()

    order_list = []

    # Gets the details of an order from a given order id
    order_details = db.query(
        'SELECT o.Order_ID, o.Staff_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE o.Staff_ID = %s AND od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID',
        [staff_id])

    if order_details:
        order_id = -1

        for ingredient in order_details:

            if ingredient["Order_ID"] != order_id:
                if order_id != -1:
                    print("Appending order")
                    order_individual["item_details_list"] = stockdetails
                    # Append the order object to the orders_list
                    order_list.append(order_individual)

                order_id = ingredient["Order_ID"]

                metadata = {}

                for key in ingredient:
                    metadata[key] = ingredient[key]

                print(metadata)

                order_individual = {"order_details_list": metadata}
                stockdetails = {}

                itemNumber = ingredient['Order_Details_ID']
                stockdetails[str(itemNumber)] = []
                stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                prev = itemNumber

            else:
                itemNumber = ingredient['Order_Details_ID']
                if itemNumber != prev:
                    order_individual["item_details_list"] = stockdetails
                    stockdetails[str(itemNumber)] = []
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                    prev = itemNumber
                else:
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])

        order_individual["item_details_list"] = stockdetails
        order_list.append(order_individual)

        return Response(json.dumps(order_list))

    else:
        return Response(json.dumps({'order_details_list': 'None'}))

@app.route('/order/list/all', methods=["GET"])
def allOrders():
    # Setup database connection
    db = MySQL_Database()

    order_list = []

    # Gets the details of an order from a given order id
    order_details = db.query(
        'SELECT o.Order_ID, o.Customer_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID',
        [])

    if order_details:
        order_id = -1

        for ingredient in order_details:

            if ingredient["Order_ID"] != order_id:
                if order_id != -1:
                    order_individual["item_details_list"] = stockdetails
                    # Append the order object to the orders_list
                    order_list.append(order_individual)

                order_id = ingredient["Order_ID"]

                metadata = {}

                for key in ingredient:
                    metadata[key] = ingredient[key]

                print(metadata)

                order_individual = {"order_details_list": metadata}
                stockdetails = {}

                itemNumber = ingredient['Order_Details_ID']
                stockdetails[str(itemNumber)] = []
                stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                prev = itemNumber

            else:
                itemNumber = ingredient['Order_Details_ID']
                if itemNumber != prev:
                    order_individual["item_details_list"] = stockdetails
                    stockdetails[str(itemNumber)] = []
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                    prev = itemNumber
                else:
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])

        order_individual["item_details_list"] = stockdetails
        order_list.append(order_individual)

        return Response(json.dumps(order_list))

    else:
        return Response(json.dumps({'order_details_list': 'None'}))

@app.route('/order/list/recent/last_month', methods=["GET"])
def getRecentOrders():
    # Setup database connection
    db = MySQL_Database()

    order_list = []

    # Gets the details of an order from a given order id
    order_details = db.query(
        'SELECT o.Order_ID, o.Customer_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID AND o.DateTime >= DATE_SUB(NOW(), INTERVAL 1 MONTH)',
        [])

    if order_details:
        order_id = -1

        for ingredient in order_details:

            if ingredient["Order_ID"] != order_id:
                if order_id != -1:
                    print("Appending order")
                    order_individual["item_details_list"] = stockdetails
                    # Append the order object to the orders_list
                    order_list.append(order_individual)

                order_id = ingredient["Order_ID"]

                metadata = {}

                for key in ingredient:
                    metadata[key] = ingredient[key]

                print(metadata)

                order_individual = {"order_details_list": metadata}
                stockdetails = {}

                itemNumber = ingredient['Order_Details_ID']
                stockdetails[str(itemNumber)] = []
                stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                prev = itemNumber

            else:
                itemNumber = ingredient['Order_Details_ID']
                if itemNumber != prev:
                    order_individual["item_details_list"] = stockdetails
                    stockdetails[str(itemNumber)] = []
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                    prev = itemNumber
                else:
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])

        order_individual["item_details_list"] = stockdetails
        order_list.append(order_individual)

        return Response(json.dumps(order_list))

    else:
        return Response(json.dumps({'order_details_list': 'None'}))


@app.route('/order/list/status/<int:order_status>', methods=["GET"])
def orderByStatus(order_status):
    # Setup database connection
    db = MySQL_Database()

    if order_status == 3:
        print("Check for completed orders")
        order_status = -1

    order_list = []

    # Gets the details of an order from a given order id
    order_details = db.query(
        'SELECT o.Order_ID, o.Customer_ID, o.Staff_ID, o.DateTime, o.Status, od.Order_Details_ID, s.Stock_ID FROM orders AS o, order_details AS od, stock AS s, item_details AS id WHERE o.status = %s AND od.Order_ID = o.Order_ID AND id.Order_Details_ID = od.Order_Details_ID AND id.Stock_ID = s.Stock_ID',
        [order_status])

    if order_details:
        order_id = -1

        for ingredient in order_details:

            if ingredient["Order_ID"] != order_id:
                if order_id != -1:
                    print("Appending order")
                    order_individual["item_details_list"] = stockdetails
                    # Append the order object to the orders_list
                    order_list.append(order_individual)

                order_id = ingredient["Order_ID"]

                metadata = {}

                for key in ingredient:
                    metadata[key] = ingredient[key]

                print(metadata)

                order_individual = {"order_details_list": metadata}
                stockdetails = {}

                itemNumber = ingredient['Order_Details_ID']
                stockdetails[str(itemNumber)] = []
                stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                prev = itemNumber

            else:
                itemNumber = ingredient['Order_Details_ID']
                if itemNumber != prev:
                    order_individual["item_details_list"] = stockdetails
                    stockdetails[str(itemNumber)] = []
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])
                    prev = itemNumber
                else:
                    stockdetails[str(itemNumber)].append(ingredient['Stock_ID'])

        order_individual["item_details_list"] = stockdetails
        order_list.append(order_individual)

        return Response(json.dumps(order_list))

    else:
        return Response(json.dumps({'order_details_list': 'None'}))

# Java access provided
@app.route('/staff/username/<username>')
def getStaffByUsername(username):
    db = MySQL_Database()
    staff_details = db.query('SELECT s.Staff_ID, s.Username, s.Iterations, s.Salt, s.PassHash, st.Staff_Type FROM staff AS s, staff_type AS st WHERE s.Staff_Type_ID = st.Staff_Type_ID AND s.Username = %s', [username])

    if staff_details:
        return Response(json.dumps(staff_details[0]))
    else:
        return Response(json.dumps({'Staff_ID': 'Void'}))


# Java access provided
@app.route('/staff/staff_id/<staff_id>')
def getStaffById(staff_id):
    db = MySQL_Database()
    staff_details = db.query('SELECT s.Staff_ID, s.Username, s.Iterations, s.Salt, s.PassHash, st.Staff_Type FROM staff AS s, staff_type AS st WHERE s.Staff_Type_ID = st.Staff_Type_ID AND s.Staff_ID = %s', [staff_id])

    if staff_details:
        return Response(json.dumps(staff_details[0]))
    else:
        return Response(json.dumps({'Staff_ID': 'Void'}))


# Java access provided
@app.route('/staff/staff_type/<staff_type>')
def getStaffByType(staff_type):
    db = MySQL_Database()
    staff_details = db.query('SELECT s.Staff_ID, s.Username, s.Iterations, s.Salt, s.PassHash, st.Staff_Type FROM staff AS s, staff_type AS st WHERE s.Staff_Type_ID = st.Staff_Type_ID AND st.Staff_Type = %s', [staff_type])

    if staff_details:
        return Response(json.dumps(staff_details))
    else:
        return Response(json.dumps({'Staff_ID': 'Void'}))


# Java access provided
@app.route('/staff/add', methods=["POST"])
def addStaff():
    staff_json = request.get_json(silent=True)

    username = staff_json['Username']
    stafftype = staff_json['Staff_Type']
    iterations = staff_json['Iterations']
    salt = staff_json['Salt']
    password = staff_json['PassHash']

    db = MySQL_Database()
    insertion_status = db.insertAndLeaveOpen('INSERT INTO staff(Username, Staff_Type_ID, Iterations, Salt, PassHash) VALUES (%s, %s, %s, %s, %s)', [username, stafftype, iterations, salt, password])

    if insertion_status:
        return Response(json.dumps({'Staff member': 'Added'}))
    else:
        return Response(json.dumps({'Staff member': 'Addition failed'}))

# Java access provided
@app.route('/customer/add', methods=["POST"])
def addCustomer():
    customer_json = request.get_json(silent=True)

    username = customer_json['Username']
    email = customer_json['Email']
    phone = customer_json['Phone_Number']
    iterations = customer_json['Iterations']
    salt = customer_json['Salt']
    password = customer_json['PassHash']
    passpin = customer_json['PassPin']
    cardtoken = customer_json['Card_Token']

    db = MySQL_Database()
    insertion_status = db.insertAndLeaveOpen('INSERT INTO Customer(Username, Email, Phone_Number, Iterations, Salt, PassHash) VALUES (%s, %s, %s, %s, %s, %s)', [username, email, phone, iterations, salt, password])

    if insertion_status:
        return Response(json.dumps({'Customer' : 'Added'}))
    else:
        return  Response(json.dumps({'Customer' : 'Addition failed'}))

# Java access provided
@app.route('/ingredients/restock', methods=["POST"])
def restockIngredient():
    ingredient_json = request.get_json(silent=True)

    stock_id = ingredient_json['stock_ID']
    restock_amount = ingredient_json['amount']

    db = MySQL_Database()
    update_status = db.update('UPDATE Stock SET Stock_Level = Stock_Level + %s WHERE Stock_ID = %s', [restock_amount, stock_id])

    if update_status:
        return Response(json.dumps({'Stock': 'Updated'}))
    else:
        return Response(json.dumps({'Stock': 'Update failed'}))

# Java access provided
@app.route("/order/assign", methods=["POST"])
def assignOrderToStaff():

    order_processing_json = request.get_json(silent=True)

    order_id = order_processing_json["order_ID"]
    staff_id = order_processing_json["staff_ID"]

    db = MySQL_Database()
    update_status = db.update('UPDATE orders SET Staff_ID = %s, Status = 1 WHERE Order_ID = %s;', [staff_id, order_id])

    if update_status:
        return Response(json.dumps({'Order Status': 'Updated'}))
    else:
        return Response(json.dumps({'Order Status': 'Update Error'}))

# Java access provided
@app.route("/order/complete/<int:order_id>")
def completeOrder(order_id):

    db = MySQL_Database()
    update_status = db.update('UPDATE orders SET Status = 2 WHERE Order_ID = %s;', [order_id])

    if update_status:
        return Response(json.dumps({'Order Status': 'Completed'}))
    else:
        return Response(json.dumps({'Order Status': 'Update Error'}))

@app.route("/customer/save/payment", methods=["POST"])
def savePaymentDetails():

    paymentDetails_json = request.get_json(silent=True)

    customer_id = paymentDetails_json["customer_id"]
    print(customer_id)
    pin = paymentDetails_json["pass_pin"]
    print(pin)
    token = paymentDetails_json["card_token"]
    print(token)

    db = MySQL_Database()
    update = db.insertAndLeaveOpen('UPDATE customer SET PassPin = %s WHERE Customer_ID = %s', [pin, customer_id])
    update = db.insert('UPDATE customer SET Card_Token = %s WHERE Customer_ID = %s', [token, customer_id])
    if update:
        return Response(json.dumps({'Customer Details': 'Updated'}))
    else:
        return Response(json.dumps({'Customer Details': 'Update failed'}))


@app.route("/customer/token/<int:user_id>")
def getToken(user_id):
    db = MySQL_Database()

    token = db.query('SELECT Card_Token FROM customer WHERE customer.Customer_ID = %s', [user_id])

    if token:
        return Response(json.dumps(token[0]))
    else:
        return Response(json.dumps({'Customer': 'void'}))

if __name__ == '__main__':
    app.run()