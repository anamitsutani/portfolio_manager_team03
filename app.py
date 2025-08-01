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

def get_amount_by_ticker(cursor):
    cursor.execute("SELECT Ticker, cast(sum(Amount) AS SIGNED) as TotalAmount FROM transactions GROUP BY Ticker")
    tickers = cursor.fetchall()
    return tickers

def calc_daily_gain(holdings):
    # get yesterday's closing prices of currently-held assets
    tickers = [h.ticker for h in holdings]
    ticker_str = " ".join(tickers)
    
    data = yf.download(ticker_str, period = '2d', interval = '1d', group_by = 'ticker')
    prev_prices = {}
    for h in holdings:
        t = h.ticker
        
        prev_price = data[(t, 'Close')].iloc[0]
        prev_prices[t] = prev_price
        
    # calculate daily gain/loss per asset type
    prev_portfolio_val = 0
    total_gain = 0
    
    for h in holdings:
        ticker = h.ticker
        amount = h.total_value
        
        prev_price = prev_prices[ticker]
        curr_price = h.current_price
        
        prev_value = amount * prev_price
        curr_value = amount * curr_price
        
        gain = curr_value - prev_value
        prev_portfolio_val += prev_value
        total_gain += gain
        
    gain_percent = (total_gain / prev_portfolio_val) * 100
    
    return total_gain, gain_percent
  
@app.route("/", methods=["GET"])
def index():
    conn, cursor = start_conn()
    tickers = get_amount_by_ticker(cursor)
    portfolio = Portfolio(tickers)
    daily_gain, gain_percent = calc_daily_gain(portfolio.holdings)
    close_conn(conn)
    return render_template('portfolio.html', holdings=portfolio.holdings, current_value=portfolio.get_portfolio_value(), daily_gain=daily_gain, gain_percent=gain_percent)

@app.route("/buy", methods=["GET"])
def buy():
    return render_template('buy.html', action_type="buy")


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)