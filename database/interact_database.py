from datetime import datetime

import mysql.connector
import pandas as pd

db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "n3u3da!",
        database = "portfolio_mgmt"
    )
cursor = db.cursor()

def update_balance_db(uuid):
    """
        Inserts a new record with updated balance into balances table based on new transactions and updates
        BalanceFlag to flag that the transaction was already accounted in the most recent balance.

        Parameters:
            UUID (int): user unique id
    """
    query_transactions_total = f"""
        SELECT (Amount*PriceAtTransaction) AS TotalPrice, ID 
        FROM transactions
        WHERE UUID={uuid} AND BalanceFlag=0;"""
    cursor.execute(query_transactions_total)
    uncommited_transactions = cursor.fetchall()

    if len(uncommited_transactions)<=0:
        return

    delta = sum([transaction[0] for transaction in uncommited_transactions])
    updated_balance = get_balance(uuid) - delta
    query_update_balance = f"INSERT INTO balance (UUID, LastUpdatedAt, Balance) VALUES ({uuid}, NOW(), {updated_balance});"
    cursor.execute(query_update_balance)

    uncommited_ids = ', '.join([str(int(transaction[1])) for transaction in uncommited_transactions])
    query_update_flags = f"UPDATE transactions SET BalanceFlag=1 WHERE ID IN ({uncommited_ids});"
    cursor.execute(query_update_flags)

    db.commit()

    return updated_balance

def get_balance(uuid):
    """
        Gets the balance from a given user from balances table in the portfolio_mgmt database.

        Parameters:
            UUID (int): user unique id
    """
    query = f"SELECT Balance FROM balance where UUID={uuid} ORDER BY LastUpdatedAt DESC LIMIT 1"

    cursor.execute(query)

    return cursor.fetchall()[0][0]

def get_all_records():
    """
    Gets all records in the Transactions table. 

    Returns:
        Pandas DataFrame with all records in the Transactions table from the portfolio_mgmt database
    """
    
    query = "SELECT * FROM Transactions"

    cursor.execute(query)

    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(result, columns = columns)

    return df

def delete_transaction(id):
    """
    Deletes a transaction with id from the Transactions table in the portfolio_mgmt database.
    """

    query = f"DELETE FROM Transactions WHERE id = {id}"

    cursor.execute(query)
    db.commit()

def place_order_db(uuid, order):
    insert_transaction(uuid, order.t_id, order.ticker, order.qty, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), order.price_at_transaction)

def insert_transaction(uuid, id, ticker, amount, transactionTimestamp, priceAtTransaction):
    """
    Inserts a record into the Transactions table in the portfolio_mgmt database. 
    
    Parameters:
        id (int): transaction id
        ticker (str): Ticker in the transaction (including the quotation marks in the string)
        amount (int): amount that was sold or bought indicated by a negative or positive value, respectively
        transactionTimestamp (str): timestamp 'YYYY-MM-DD HH:MM:SS' of when the transaction occurred (including the quotation marks in the string)
        priceAtTransaction (float): price of the asset in the transaction
    """
    
    query = f"""
            INSERT INTO Transactions (ID, UUID, Ticker, Amount, TransactionTimestamp, PriceAtTransaction)
            VALUES ({id}, {uuid},\"{ticker}\", {amount}, \"{transactionTimestamp}\", {priceAtTransaction})
            """
    cursor.execute(query)
    db.commit()