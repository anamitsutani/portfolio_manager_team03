import yfinance as yf
from models.holding import Holding
import pandas as pd

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
        
        if ticker_str:
            data = yf.download(ticker_str, period = '2d', interval = '1d', group_by = 'ticker')
        else:
            return 0, 0
        
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
    
    def calc_unrealized_gain(self, transactions):
        if not transactions:
            return 0, 0
        
        total_unrealized = 0
        unrealized_percent = 0
        total_cost_basis = 0
        total_current_value = 0
        df = pd.DataFrame(transactions)
        df = df[df['Amount'] > 0]
        df['Cost'] = df['Amount'] * df['PriceAtTransaction']
        for h in self.holdings:
            ticker = h.ticker
            df_ticker = df[df['Ticker'] == ticker]
            total_shares = h.qty
            avg_cost_share = df_ticker['Cost'].sum() / total_shares
            current_value = h.total_value
            cost_basis = avg_cost_share * total_shares
            unrealized_gain = current_value - float(cost_basis)
            
            total_unrealized += unrealized_gain
            total_cost_basis += cost_basis
            total_current_value += current_value
        
        unrealized_percent = ((total_current_value - float(total_cost_basis)) / float(total_cost_basis)) * 100
        return total_unrealized, unrealized_percent
    