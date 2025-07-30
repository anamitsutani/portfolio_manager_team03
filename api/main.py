from flask import Flask, request
from flask_restful import Resource, Api
import yfinance as yf
import requests

app = Flask(__name__)
api = Api(app)

class Stock(Resource):
    def get(self):
        symbol = request.args.get("symbol")

        if not symbol:
            return {"error": "Missing 'symbol' query parameter"}, 400

        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            if 'regularMarketPrice' not in info:
                return {"error": f"Ticker '{symbol}' not found"}, 404
            data = {
                "symbol": symbol.upper(),
                "price": info.get("currentPrice", "N/A"),
                "market_cap": info.get("marketCap", "N/A"),
                "high_52": info.get("fiftyTwoWeekHigh", "N/A"),
                "low_52": info.get("fiftyTwoWeekLow", "N/A")
            }
            return data, 200
        except Exception as e:
            return {"error": str(e)}, 500

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

api.add_resource(Stock, '/stock')
api.add_resource(History, '/history')

if __name__ == '__main__':
    app.run(debug=True)