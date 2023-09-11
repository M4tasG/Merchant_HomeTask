from flask import Flask
from flask import render_template
from flask import request
import requests
import json

with open('config.json', 'r') as f:
    config = json.load(f)

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template('index.html')

@app.route("/create-order/")
def create_order():
    payload = {}
    if request.args.get('amount'):
        payload = {
            "amount": float(request.args.get("amount")) * 100,
            "currency": "GBP",
            "email": "example.customer@email.com"
        }
    else:
        payload = {
            "amount": 100,
            "currency": "GBP",
            "email": "example.customer@email.com"
        }  
    url = "https://sandbox-merchant.revolut.com/api/1.0/orders"
    headers = {
        "Authorization": f'Bearer {config["SANDBOX_SECRET_KEY"]}'
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 201:
        return response.json()
    else:
        return {"Error": "Something went wrong"}

@app.route("/checkout/")
def checkout_page():
    return render_template('checkout.html')

@app.route("/checkout-variable/")
def checkout_variable_page():
    return render_template('checkout_variable.html')

@app.route("/order-success/")
def order_success():
    order_id = request.args.get("order_id")
    return render_template('success.html', order_id=order_id)

@app.route("/order-failed/")
def order_failed():
    error_message = request.args.get("message")
    return render_template('error.html', error_message=error_message)