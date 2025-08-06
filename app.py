from flask import Flask, render_template
import mysql.connector
from models.portfolio import Portfolio
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

def get_amount_by_ticker(cursor, uuid):
    cursor.execute(f"SELECT Ticker, cast(sum(Amount) AS SIGNED) as TotalAmount FROM transactions WHERE UUID={uuid} GROUP BY Ticker")
    tickers = cursor.fetchall()
    return tickers
  
@app.route("/", methods=["GET"])
def index():
    conn, cursor = start_conn()
    user_id = 1
    tickers = get_amount_by_ticker(cursor, user_id)
    portfolio = Portfolio(tickers)
    daily_gain, gain_percent = portfolio.calc_daily_gain()
    transactions = get_transactions(cursor)
    unrealized, unrealized_percent = portfolio.calc_unrealized_gain(transactions)
    pnl = portfolio.calc_pnl(transactions)
    close_conn(conn)
    return render_template('portfolio.html',
                           user_id = user_id,
                           holdings=portfolio.holdings,
                           current_value=portfolio.get_portfolio_value(),
                           daily_gain=daily_gain,
                           gain_percent=gain_percent,
                           total_unrealized=unrealized,
                           unrealized_percent=unrealized_percent,
                           pnl = pnl
                           )

@app.route("/trade", methods=["GET"])
def trade():
    return render_template('trade.html')


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)