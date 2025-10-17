# import os
import re
import datetime

from TransactionParser import parseEmailData, ChaseParser
from Transaction import Transaction
from MailReader import MailReader
from Ledger import Ledger

IMAP_SERVER = "imap.gmail.com"
LABEL = 'Banking/ChaseCharges'
CREDSFILE = 'credentials.txt'

PARSER = ChaseParser

DATABASE_FILE = "transactions.db"

# PLACEHOLDER VALUE
# need to refine this a LOT later (for categories)
MONTHLY_BUDGET = 1050.0

def main():
    print(f"Reading credentials file {CREDSFILE}")
    # read in the username and password
    with open(CREDSFILE, 'r') as credsfile:
        username = credsfile.readline().strip()
        password = credsfile.readline().strip()

    if not username or not password:
        raise f"Need to fill in credentials file `{CREDSFILE}` with username and password for IMAP server"


    print("Logging in...")
    mailReader = MailReader(username, password, LABEL, IMAP_SERVER)

    
    print("Reading mail")
    newEmailSubjectsAndTimes = mailReader.readUnreadSubjectsAndTimes()


    print(f"Parsing {len(newEmailSubjectsAndTimes)} emails")
    transactions = set()
    for (subject, date_time) in newEmailSubjectsAndTimes:
        try:
            amount, merchant = parseEmailData(PARSER, subject)
        except ValueError:
            print("Failed to parse! Skipping")
            continue 

        transactions.add(Transaction(amount, merchant, date_time))

    print(f"Updating databse with {len(transactions)}")
    ledger = Ledger(DATABASE_FILE)
    ledger.update_ledger(transactions)

    transactions = ledger.get_transactions_past_days(30)

    spent = sum([t.amount for t in transactions])
    print(f"Spent this past month: {spent}")

    percent = spent/MONTHLY_BUDGET * 100.0

    print(f"Percent spent this month: {percent:.2f}%")

if __name__ == "__main__":
    main()
