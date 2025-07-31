from flask import Flask, request, render_template
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('portfolio.html')

@app.route("/buy", methods=["GET"])
def buy():
    return render_template('buy.html')

@app.route("/sell", methods=["GET"])
def sell():
    return render_template('sell.html')

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5001)