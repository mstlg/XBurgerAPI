from flask import Flask, url_for, json, Response
from mysql_db import MySQL_Database
import os

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



if __name__ == '__main__':
    app.run()
