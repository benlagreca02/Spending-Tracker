
import imaplib
import email
from email.header import decode_header
import os
import re

IMAP_SERVER="imap.gmail.com"
LABEL='Banking/ChaseCharges'
CREDSFILE = 'credentials.txt'

print(f"Reading credentials file {CREDSFILE}")
# read in the username and password
with open(CREDSFILE, 'r') as credsfile:
    username = credsfile.readline().strip()
    password = credsfile.readline().strip()

if not username or not password:
    raise f"Need to fill in credentials file `{CREDSFILE}` with username and password"


print(f"Reading messages from {LABEL}")
status, messages = imap.select(mailbox=LABEL)
messages = int(messages[0])  # num messages

print(f"Found {messages} emails in label 'chase'")

# Create a directory to save emails
# os.makedirs("emails", exist_ok=True)

# Fetch emails in order of oldest to newest 
for i in range(messages, 0, -1):
    status, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # Parse email
            msg = email.message_from_bytes(response[1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding if encoding else "utf-8")
            # subject = subject.replace("/", "_")  # Avoid file path issues

            # Pattern explanation:
            # \$([\d.]+) → matches the dollar amount (e.g., $456.23)
            # transaction with (.+) → captures everything after "transaction with"
            pattern = r"\$(\d+(?:\.\d+)?) transaction with (.+)"

            match = re.search(pattern, subject)
            if match:
                amount = match.group(1)
                merchant = match.group(2)
                print(f"Amount: {amount}")
                print(f"Merchant: {merchant}")
            else:
                print("Pattern not found.")


            # filename = f"emails/{i}_{subject}.eml"
            # with open(filename, "wb") as f:
                # f.write(response[1])
            # print(f"Saved: {filename}")

# Logout
imap.logout()

