import sys
import os
from os.path import realpath, dirname
SRC_PATH = dirname(realpath(__file__))
sys.path.append(os.path.join(SRC_PATH, "database"))
sys.path.append(os.path.join(SRC_PATH, "models"))

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

from models.order import Order
from models.user import User
import yfinance as yf
import random

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5001"}})


def generate_id():
    return random.randint(100000000, 999999999)

def get_ticker_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    if 'currentPrice' not in info:
        return { "error": 404 }
    return {
        "symbol": ticker.upper(),
        "price": info.get("currentPrice", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "high_52": info.get("fiftyTwoWeekHigh", "N/A"),
        "low_52": info.get("fiftyTwoWeekLow", "N/A")
    }

class Stock(Resource):
    def get(self):
        ticker = request.args.get("ticker")
        if not ticker:
            return { "error": "Missing 'ticker' query parameter" }, 400
        try:
            data = get_ticker_data(ticker)
            if "error" in data:
                return { "error": f"Could not retrieve data for ticker {ticker}" }, 404
            return get_ticker_data(ticker), 200
        except Exception as e:
            return { "error": str(e) }, 500

    def post(self):
        json_data = request.get_json()
        for parameter in ["ticker", "qty", "user_id"]:
            if not json_data.get(parameter):
                return {"error": f"Missing parameter {parameter} in json request body"}, 400

        try:
            ticker = json_data.get('ticker')
            data = get_ticker_data(ticker)
            if "error" in data:
                return {"error": f"Could not retrieve data for ticker {ticker}"}, 404
            curr_price = data["price"]

            user_id = json_data.get('user_id')
            user = User(user_id)

            order = Order(generate_id(), user_id, ticker, json_data.get('qty'), curr_price)
            result = user.place_order(order)
            if "error" in result:
                return {"error": result["error"]}, 400
            return jsonify(order.to_dict())

        except Exception as e:
            return { "error": str(e) }, 500

class History(Resource):
    def get(self):
        symbol = request.args.get("symbol")
        period = request.args.get("period")

        if not symbol:
            return {"error": "Missing 'symbol' query parameter"}, 400
        if not period:
            return {"error": "Missing 'period' query parameter"}, 400

        try:
            stock = yf.Ticker(symbol)
            print(stock)
            hist = stock.history(period=period)

            if hist.empty:
                return {"error": f"Ticker '{symbol}' not found"}, 404

            hist.reset_index(inplace=True)
            hist["Date"] = hist["Date"].dt.strftime('%Y-%m-%d %H:%M:%S')
            history_data = hist.to_dict(orient="records")
            return {"symbol": symbol.upper(), "history": history_data}, 200
        except Exception as e:
            return {"error": str(e)}, 500

class Balance(Resource):
    def get(self):
        user_id = request.args.get("userId")
        if not user_id:
            return { "error": "Missing 'userId' query parameter" }, 400
        try:
            user = User(user_id)
            return { "balance": str(user.balance) }
        except Exception as e:
            return { "error": str(e) }, 500

class Portfolio(Resource):
    def get(self):
        for parameter in ["ticker", "userId"]:
            if not request.args.get(parameter):
                return {"error": f"Missing query parameter {parameter}"}, 400
        user_id = request.args.get("userId")
        ticker = request.args.get("ticker")

        try:
            user = User(user_id)
            amount = user.get_ticker_amount(ticker)
            if not amount:
                return { "error": f"User doesn't own shares of {ticker}" },404
            return { "ticker": ticker, "amount": amount }, 200
        except Exception as e:
            return { "error": str(e) }, 500


api.add_resource(Stock, '/api/stock')

api.add_resource(History, '/api/history')

api.add_resource(Balance, '/api/balance')

api.add_resource(Portfolio, '/api/portfolio')

if __name__ == '__main__':
    app.run(debug=True)