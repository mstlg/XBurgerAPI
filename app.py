from flask import Flask, url_for, json, Response

app = Flask(__name__)

# API root
@app.route('/')
def api_root():
    data = {'welcome': 'xTreme Burger API'}
    return Response(json.dumps(data))

# Customer database access
@app.route('/customer/<username>')
def customer_by_username(username):
    data = {'customer' : 'Julian'}
    return Response(json.dumps(data))

if __name__ == '__main__':
    app.run()
