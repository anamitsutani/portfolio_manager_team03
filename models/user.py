from database.interact_database import get_balance, update_balance_db, place_order_db, get_amount_by_ticker


class User:
    def __init__(self, id):
        self.id = id
        self.balance = get_balance(self.id)

    def update_balance(self):
        updated_balance = update_balance_db(self.id)
        if updated_balance:
            self.balance = updated_balance
            return self.balance
        return "Balance already up to date"

    def get_ticker_amount(self, ticker):
        amounts_dict = get_amount_by_ticker(self.id)
        if ticker in amounts_dict.keys():
            return amounts_dict[ticker]
        return None

    def place_order(self, order):
        if not self.check_has_balance(order.total_price):
            return { "error": "User has insufficient balance to place order" }
        if not self.check_has_holdings(order.ticker, order.qty):
            return { "error": f"User has insufficient stocks of {order.ticker} to place order" }
        place_order_db(self.id, order)
        return { "updated_balance": self.update_balance() }

    def check_has_balance(self, order_price):
        return (order_price<0) or (self.balance>=order_price)

    def check_has_holdings(self, ticker, qty):
        if qty>0:
            return True
        holdings = self.get_ticker_amount(ticker)
        return ("error" not in holdings.keys()) and holdings>(qty*-1)