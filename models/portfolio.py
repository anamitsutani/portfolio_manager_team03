import yfinance as yf
from models.holding import Holding

class Portfolio:
    def __init__(self, tickers):
        self.holdings = self.__get_holdings(tickers)

    def __get_holdings(self, tickers):
        holdings: [Holding] = []
        for ticker in tickers:
            symbol = ticker['Ticker']
            qty = ticker['TotalAmount']
            try:
                curr_price = yf.Ticker(symbol).info.get("currentPrice")
                holdings.append(Holding(symbol, curr_price, qty))
            except Exception as e:
                return e
        return holdings

    def get_portfolio_value(self):
        return sum(holding.total_value for holding in self.holdings)