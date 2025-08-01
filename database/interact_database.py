import mysql.connector
import pandas as pd

def get_all_records():
    """
    Gets all records in the Transactions table. 

    Returns:
        Pandas DataFrame with all records in the Transactions table from the portfolio_mgmt database
    """
    
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "n3u3da!",
        database = "portfolio_mgmt"
    )
    
    query = "SELECT * FROM Transactions"

    cursor = db.cursor()
    cursor.execute(query)

    result = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    df = pd.DataFrame(result, columns = columns)

    return df
    
    
def delete_transaction(id):
    """
    Deletes a transaction with id from the Transactions table in the portfolio_mgmt database. 
    
    """
    
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "n3u3da!",
        database = "portfolio_mgmt"
    )

    query = f"DELETE FROM Transactions WHERE id = {id}"

    cursor = db.cursor()
    cursor.execute(query)
    db.commit()


def insert_transaction(id, ticker, amount, transactionTimestamp, priceAtTransaction):
    """
    Inserts a record into the Transactions table in the portfolio_mgmt database. 
    
    Parameters:
        id (int): transaction id
        ticker (str): Ticker in the transaction (including the quotation marks in the string)
        amount (int): amount that was sold or bought indicated by a negative or positive value, respectively
        transactionTimestamp (str): timestamp 'YYYY-MM-DD HH:MM:SS' of when the transaction occurred (including the quotation marks in the string)
        priceAtTransaction (float): price of the asset in the transaction
    
    """
    
    db = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "n3u3da!",
        database = "portfolio_mgmt"
    )
    
    query = f"INSERT INTO Transactions (ID, Ticker, Amount, TransactionTimestamp, PriceAtTransaction) VALUES ({id}, \"{ticker}\", {amount}, \"{transactionTimestamp}\", {priceAtTransaction})"
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()