class Transaction:
    def __init__(self, transaction):
        self.id = transaction['UUID']
        self.ticker = transaction['Ticker']
        self.action = self.__get_action(transaction['Amount'])
        self.amount = abs(transaction['Amount'])
        self.timestamp = transaction['TransactionTimestamp']
        self.price_at_transaction = transaction['PriceAtTransaction']
        
    def __get_action(self, amount):
        if amount>0:
            return 'Buy'
        else:
            return 'Sell'
        
    def to_dict(self):
        return {
            'id': self.id,
            'ticker': self.ticker,
            'amount': self.amount,
            'timestamp': self.timestamp,
            'price_at_transaction': self.price_at_transaction
        }