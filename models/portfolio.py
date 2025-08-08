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
    
    def calc_avg_cost_basis(self, transactions):
        avg_cost_basis = {}
        transactions = pd.DataFrame(transactions)
        transactions = transactions.sort_values(by = 'TransactionTimestamp')
        
        for ticker, group in transactions.groupby('Ticker'):
            total_amount = 0
            total_cost = 0.0
            
            for _, row in group.iterrows():
                amount = row['Amount']
                price = row['PriceAtTransaction']
                
                if amount > 0:
                    # buy: increase total amount and cost
                    total_amount += amount
                    total_cost += amount * float(price)
                    
                elif amount < 0:
                    # sell: decrease quantity and cost
                    if total_amount == 0:
                        continue
                    sell_amount = -amount
                    avg_cost = total_cost / total_amount
                    total_amount -= sell_amount
                    total_cost -= sell_amount * avg_cost
                    
            if total_amount > 0:
                avg_cost_basis[ticker] = total_cost / total_amount
            else:
                avg_cost_basis[ticker] = 0     
                     
        return avg_cost_basis
    
    def calc_unrealized_gain(self, transactions):
        if not transactions:
            return 0, 0
        
        total_unrealized = 0
        unrealized_percent = 0
        total_cost_basis = 0
        total_current_price = 0
        avg_cost_basis = self.calc_avg_cost_basis(transactions)
        
        for h in self.holdings:
            ticker = h.ticker
            total_shares = h.qty
            
            cost_basis = avg_cost_basis[ticker]
            current_price = h.current_price
            unrealized_gain = (current_price - float(cost_basis)) * total_shares
            
            total_unrealized += unrealized_gain
            total_cost_basis += cost_basis
            total_current_price += current_price
        
        unrealized_percent = ((total_current_price - float(total_cost_basis)) / float(total_cost_basis)) * 100
        return total_unrealized, unrealized_percent
    
    def calc_realized_gain(self, transactions):
        if not transactions:
            return 0
        
        df = pd.DataFrame(transactions)
        df = df.sort_values(by = 'TransactionTimestamp')
        
        # track ticker open lots
        open_lots = {}
        total_realized = 0
        
        for _, row in df.iterrows():
            ticker = row['Ticker']
            amount = row['Amount']
            price = row['PriceAtTransaction']
            
            if ticker not in open_lots:
                open_lots[ticker] = []
                
            if amount > 0:
                # transaction is a buy - add to open lots
                open_lots[ticker].append({'amount': amount, 'price': price})
            else:
                sell_amount = -amount
                sell_price = price
                gain = 0
                
                while sell_amount > 0 and open_lots[ticker]:
                    lot = open_lots[ticker][0]
                    lot_amount = lot['amount']
                    lot_price = lot['price']
                    
                    if lot_amount <= sell_amount:
                        # use lot entirely
                        gain = (sell_price - lot_price) * lot_amount
                        total_realized += gain
                        sell_amount -= lot_amount
                        open_lots[ticker].pop(0)
                    else:
                        # use lot partially
                        gain = (sell_price - lot_price) * sell_amount
                        total_realized += gain
                        lot['amount'] -= sell_amount
                        sell_amount = 0           
        return total_realized
    
    def calc_pnl(self, transactions):
        if not transactions:
            return 0
        total_pnl = 0
        
        transactions = pd.DataFrame(transactions)
        tickers = set(transactions['Ticker'])
        for ticker in tickers: 
            print
            ticker_transactions = transactions[transactions['Ticker'] == ticker]
            cost = ticker_transactions['Amount'] * ticker_transactions['PriceAtTransaction']
            cost = [float(x) for x in cost]
            
            # handle leftover
            leftover_share = ticker_transactions['Amount'].sum()
            current_price = yf.Ticker(ticker).info.get("currentPrice")
            total_pnl += (-leftover_share * current_price) - sum(cost)
        
        return total_pnl