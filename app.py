from flask import Flask, url_for, json, Response
from mysql_db import MySQL_Database

app = Flask(__name__)

# API root
@app.route('/')
def api_root():
    data = {'welcome': 'xTreme Burger API'}
    return Response(json.dumps(data))

# Customer database access
@app.route('/customer/<username>', methods=["GET"])
def customer_by_username(username):

    # Setup database connection
    db = MySQL_Database()

    # Query Customer table by username and pull all information if available
    customer_information = db.query('SELECT * FROM customer WHERE customer.Username = %s', [username])

    len(customer_information)

    if len(customer_information) > 0:
        return Response(json.dumps(customer_information))
    else:
        return Response(json.dumps({"customer" : "void"}))

if __name__ == '__main__':
    app.run()
