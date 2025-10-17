import imaplib
import email
from email.header import decode_header
import datetime
from zoneinfo import ZoneInfo


# Given a username, password, label, and mailserver, log in and get/manage
# emails
class MailReader:
    # "label" is google's name for mailbox
    def __init__(self, username, password, label, server):
        self.imap = imaplib.IMAP4_SSL(server, timeout=10)
        self.imap.login(username, password)
        self.label = label

        # returns number of emails in the box as (status, [num_mails])
        self.imap.select(mailbox=self.label)
    
    def __del__(self):
        self.imap.logout()

    # Will mark found emails as read
    def readUnreadSubjectsAndTimes(self) -> set[tuple[str, datetime]]:

        # Returns space sep string, in a list of matching mail id's 
        # (status, [ids_str])
        status, ids_str = self.imap.search(None, 'UNSEEN')
        ids = ids_str[0].split()

        # we don't need order, and there is no duplicates
        subject_time_tuples = set()
        for email_id in ids:
            # (typ, [data, ...])
            # 'data' are tuples of message part envelope and data.
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')
            raw_data = msg_data[0][1]
            msg = email.message_from_bytes(raw_data)
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')
            date_as_str = msg['Date']
            datetime_from_email = email.utils.parsedate_to_datetime(date_as_str)

            subject_time_tuples.add( (subject, datetime_from_email) )
        return subject_time_tuples
