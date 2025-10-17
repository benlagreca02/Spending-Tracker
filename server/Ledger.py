
# manages reading, writing, tracking, and fetching transactions from a local
# database

from Transaction import Transaction
import sqlite3
from datetime import datetime, timedelta


class Ledger:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db_connection = sqlite3.connect(self.db_file)

    def __del__(self):
        # close the connection to the database
        print("Disconnecting from database")
        if hasattr(self, 'conn') and self.conn:
            self.db_connection.close()

    def update_ledger(self, transactions):
        # should we connect in init
        # or every time we want data from it? 
        cursor = self.db_connection.cursor()

        # Ensure table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                amount REAL,
                merchant TEXT,
                time TEXT
            )
        """)

        # Insert each transaction
        for tx in transactions:
            tx_id = tx.get_id()
            cursor.execute("""
                INSERT OR IGNORE INTO transactions (id, amount, merchant, time)
                VALUES (?, ?, ?, ?)
            """, (tx_id, tx.amount, tx.merchant, tx.timestamp.isoformat()))

        self.db_connection.commit()

    def print_all_transactions(self):
        cursor = self.db_conection.cursor()

        cursor.execute("SELECT id, amount, merchant, time FROM transactions")
        rows = cursor.fetchall()

        print("All Transactions:")
        for row in rows:
            tx_id, amount, merchant, time = row
            print(f"ID: {tx_id}\nAmount: ${amount:.2f}\nMerchant: {merchant}\nTime: {time}\n---")

        conn.close()

    def get_transactions_this_month(self):
        cursor = self.db_connection.cursor()

        now = datetime.now()
        year, month = now.year, now.month
        start_of_month = f"{year}-{month:02d}-01T00:00:00"
        if month == 12:
            end_of_month = f"{year + 1}-01-01T00:00:00"
        else:
            end_of_month = f"{year}-{month + 1:02d}-01T00:00:00"
        cursor.execute("""
            SELECT * FROM transactions
            WHERE time >= ? AND time < ?
            """, (start_of_month, end_of_month))

        return self.reconstruct_transactions(cursor.fetchall())


    def get_transactions_past_days(self, num_days):
        cursor = self.db_connection.cursor()
        now = datetime.now()
        num_days_ago = (now - timedelta(days=num_days)).isoformat()

        cursor.execute(""" 
                SELECT amount, merchant, time FROM transactions 
                WHERE time >= ?  """, (num_days_ago,))

        return self.reconstruct_transactions(cursor.fetchall())


    @staticmethod
    def reconstruct_transactions(fetched):
        # We really don't need to construct/fetch the ID, its really just for
        # uniqueness the SQL Database
        return {Transaction(amount, merchant, datetime.fromisoformat(timestamp)) 
                for amount, merchant, timestamp in fetched}

