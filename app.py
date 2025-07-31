from flask import Flask, request, render_template
import mysql.connector
import yfinance as yf

app = Flask(__name__)

def get_holdings():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="n3u3da!",
        database="portfolio_mgmt"
    )
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM transactions")
    data = cursor.fetchall()
    conn.close()
    return data

def calc_value(holdings):
    total = []
    print(holdings)
    for holding in holdings:
        symbol = holding['Ticker']
        try:
            stock = yf.Ticker(symbol)
            total.append(stock.info.get("currentPrice"))
        except Exception as e:
            return {"error": str(e)}, 500
    return sum(total)

@app.route("/", methods=["GET"])
def index():
    holdings = get_holdings()
    print(holdings)
    print(calc_value(holdings))
    return render_template('portfolio.html', holdings=holdings)

if __name__ == "__main__":
    app.run()