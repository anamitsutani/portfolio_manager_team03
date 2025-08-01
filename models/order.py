class Order:
    def __init__(self, t_id, ticker, qty, price_at_transaction):
        self.t_id = t_id,
        self.ticker = ticker
        self.qty = qty
        self.price_at_transaction = price_at_transaction
        self.total_price = qty * price_at_transaction

    def to_dict(self):
        return {
            "id": self.t_id,
            "ticker": self.ticker,
            "qty": self.qty,
            "price_at_transaction": self.price_at_transaction,
            "total_price": self.total_price
        }