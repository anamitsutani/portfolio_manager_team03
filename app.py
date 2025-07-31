from flask import Flask, request, render_template
import mysql.connector
import yfinance as yf

app = Flask(__name__)

def start_conn():
    conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="n3u3da!",
            database="portfolio_mgmt"
        )
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

def close_conn(conn):
    conn.close()

def get_transactions(cursor):
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()
    return data

def get_amount_by_ticker(cursor):
    cursor.execute("SELECT Ticker, cast(sum(Amount) AS SIGNED) as TotalAmount FROM transactions GROUP BY Ticker")
    tickers = cursor.fetchall()
    return tickers

def get_holdings(tickers):
    holdings = []
    for ticker in tickers:
        symbol = ticker['Ticker']
        qty = ticker['TotalAmount']
        try:
            stock = yf.Ticker(symbol)
            ticker["CurrPrice"] = stock.info.get("currentPrice")
            ticker['TotalValue'] = qty * ticker["CurrPrice"]
            holdings.append(ticker)
        except Exception as e:
            return {"error": str(e)}, 500
    return holdings

def get_portfolio_value(holdings):
    return sum(ticker.get('TotalValue') for ticker in holdings)

@app.route("/", methods=["GET"])
def index():
    conn, cursor = start_conn()
    tickers = get_amount_by_ticker(cursor)
    holdings = get_holdings(tickers)
    close_conn(conn)
    return render_template('portfolio.html', holdings=holdings, current_value=get_portfolio_value(holdings))

@app.route("/buy", methods=["GET"])
def buy():
    return render_template('buy.html', action_type="buy")

@app.route("/sell", methods=["GET"])
def sell():
    return render_template('sell.html', action_type="sell")

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)