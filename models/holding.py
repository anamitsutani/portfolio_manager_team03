class Holding:
    def __init__(self, ticker: str, current_price: float, qty: int):
        self.ticker = ticker
        self.current_price = current_price
        self.qty = qty
        self.total_value = current_price * qty