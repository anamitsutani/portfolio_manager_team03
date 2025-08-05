from database.interact_database import get_balance, update_balance_db, place_order_db


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

    def place_order(self, order):
        if not self.check_has_balance(order.total_price):
            return
        place_order_db(self.id, order)
        return self.update_balance()

    def check_has_balance(self, order_price):
        return (order_price<0) or (self.balance>=order_price)