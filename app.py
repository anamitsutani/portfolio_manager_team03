from flask import Flask, request, render_template
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template('portfolio.html')

if __name__ == "__main__":
    app.run()