class Order:
    def __init__(self, t_id: int, uuid: int, ticker: str, qty: int, price_at_transaction: float):
        self.t_id = t_id
        self.uuid = uuid
        self.ticker = ticker
        self.qty = qty
        self.price_at_transaction = price_at_transaction
        self.total_price = qty * price_at_transaction

    def to_dict(self):
        return {
            "id": self.t_id,
            "uuid": self.uuid,
            "ticker": self.ticker,
            "qty": self.qty,
            "price_at_transaction": self.price_at_transaction,
            "total_price": self.total_price
        }