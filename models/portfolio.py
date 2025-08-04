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
    
    def calc_daily_gain(self):
        # get yesterday's closing prices of currently-held assets
        tickers = [h.ticker for h in self.holdings]
        ticker_str = " ".join(tickers)
        
        data = yf.download(ticker_str, period = '2d', interval = '1d', group_by = 'ticker')
        prev_prices = {}
        for h in self.holdings:
            t = h.ticker
            
            prev_price = data[(t, 'Close')].iloc[0]
            prev_prices[t] = prev_price
            
        # calculate daily gain/loss per asset type
        prev_portfolio_val = 0
        total_gain = 0
        
        for h in self.holdings:
            ticker = h.ticker
            amount = h.qty
            
            prev_price = prev_prices[ticker]
            curr_price = h.current_price
            
            prev_value = amount * prev_price
            curr_value = amount * curr_price
            
            gain = curr_value - prev_value
            prev_portfolio_val += prev_value
            total_gain += gain
            
        gain_percent = (total_gain / prev_portfolio_val) * 100
        
        return total_gain, gain_percent
    
    