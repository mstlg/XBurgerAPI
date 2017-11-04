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
        return Response(json.dumps({"customer": "void"}))


if __name__ == '__main__':
    app.run()
