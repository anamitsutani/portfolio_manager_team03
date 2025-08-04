from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS

from models.order import Order
from database.interact_database import insert_transaction
from datetime import datetime
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
    if 'regularMarketPrice' not in info:
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

        ticker = json_data.get('ticker')
        qty = json_data.get('qty')
        t_id = generate_id()
        try:
            data = get_ticker_data(ticker)
            if "error" in data:
                return {"error": f"Could not retrieve data for ticker {ticker}"}, 404
            curr_price = data["price"]
            order = Order(t_id, ticker, qty, curr_price)
            insert_transaction(t_id, ticker, qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), curr_price)
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
            hist = stock.history(period=period)

            if hist.empty:
                return {"error": f"Ticker '{symbol}' not found"}, 404

            hist.reset_index(inplace=True)
            hist["Date"] = hist["Date"].dt.strftime('%Y-%m-%d %H:%M:%S')
            history_data = hist.to_dict(orient="records")
            return {"symbol": symbol.upper(), "history": history_data}, 200
        except Exception as e:
            return {"error": str(e)}, 500

api.add_resource(Stock, '/api/stock')

api.add_resource(History, '/api/history')

if __name__ == '__main__':
    app.run(debug=True)