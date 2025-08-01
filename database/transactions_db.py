import mysql.connector

class TransactionsDb:
    def __init__(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="n3u3da!",
            database="portfolio_mgmt"
        )
        self.cursor = self.db.cursor()

    def execute_select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def execute_insert_or_delete(self, query):
        self.cursor.execute(query)
        self.db.commit()

    def close_conn(self):
        self.db.close()