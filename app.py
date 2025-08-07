from flask import Flask, render_template, jsonify
import mysql.connector
from models.portfolio import Portfolio
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

from models.transaction import Transaction

from models.transaction import Transaction

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

def get_transactions(cursor, user):
    cursor.execute(f"SELECT * FROM transactions where UUID={user} ORDER BY TransactionTimestamp DESC")
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
    transactions = get_transactions(cursor, user_id)
    lastest_transactions = [Transaction(transaction) for transaction in transactions[0:5]]
    unrealized, unrealized_percent = portfolio.calc_unrealized_gain(transactions)
    pnl = portfolio.calc_pnl(transactions)
    close_conn(conn)
    return render_template('portfolio.html',
                           user_id = user_id,
                           holdings=portfolio.holdings,
                           current_value=portfolio.get_portfolio_value(),
                           lastest_transactions=lastest_transactions,
                           daily_gain=daily_gain,
                           gain_percent=gain_percent,
                           total_unrealized=unrealized,
                           unrealized_percent=unrealized_percent,
                           pnl=pnl
                           )

@app.route("/trade", methods=["GET"])
def trade():
    return render_template('trade.html')

@app.route("/api/portfolio/performance", methods=["GET"])
def get_portfolio_performance():
    try:
        # get user's portfolio holdings
        conn, cursor = start_conn()
        user_id = 1  
        tickers = get_amount_by_ticker(cursor, user_id)
        
        if not tickers:
            return jsonify({"error": "No holdings found"}), 404
        
        # get historical data for all tickers in the portfolio
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        

        portfolio_history = {}
        
        for ticker_data in tickers:
            ticker = ticker_data['Ticker']
            shares = ticker_data['TotalAmount']
            
            # get historical data for the ticker
            stock = yf.Ticker(ticker)
            hist = stock.history(start=start_date, end=end_date)
            
            if not hist.empty:
                # calculate daily position value
                for date, row in hist.iterrows():
                    date_str = date.strftime('%m-%d')
                    if date_str not in portfolio_history:
                        portfolio_history[date_str] = 0
                    portfolio_history[date_str] += row['Close'] * shares
        

        dates = sorted(portfolio_history.keys())
        values = [portfolio_history[date] for date in dates]
        
        close_conn(conn)
        return jsonify({
            "dates": dates,
            "values": values
        })
        
    except Exception as e:
        print(f"Error fetching portfolio performance: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)