from flask import Flask, render_template
import mysql.connector
from models.portfolio import Portfolio

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

@app.route("/", methods=["GET"])
def index():
    conn, cursor = start_conn()
    tickers = get_amount_by_ticker(cursor)
    portfolio = Portfolio(tickers)
    close_conn(conn)
    return render_template('portfolio.html', holdings=portfolio.holdings, current_value=portfolio.get_portfolio_value())


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)