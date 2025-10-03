# import os
import re
from MailReader import MailReader
import datetime

IMAP_SERVER="imap.gmail.com"
LABEL='Banking/ChaseCharges'
CREDSFILE = 'credentials.txt'


def main():
    print(f"Reading credentials file {CREDSFILE}")
    # read in the username and password
    with open(CREDSFILE, 'r') as credsfile:
        username = credsfile.readline().strip()
        password = credsfile.readline().strip()

    if not username or not password:
        raise f"Need to fill in credentials file `{CREDSFILE}` with username and password"


    print("Logging in...")
    mailReader = MailReader(username, password, LABEL, IMAP_SERVER)

    
    print("Reading mail")
    newEmailSubjectsAndTimes = mailReader.readUnreadMailSubjectsAndDates()


    print(f"Got {len(newEmailSubjectsAndTimes)} emails!")

    pattern = r"\$(\d+(?:\.\d+)?) transaction with (.+)"

    for (subject, date_time) in newEmailSubjectsAndTimes:

        match = re.search(pattern, subject)
        if match:
            amount = match.group(1)
            merchant = match.group(2)
            # t = datetime.datetime(2012, 2, 23, 0, 0)
            print(f"{amount} @ {merchant} on {date_time.strftime('%m/%d/%Y')}")

            # filename = f"emails/{i}_{subject}.eml"
            # with open(filename, "wb") as f:
                # f.write(response[1])
            # print(f"Saved: {filename}")



if __name__ == "__main__":
    main()
