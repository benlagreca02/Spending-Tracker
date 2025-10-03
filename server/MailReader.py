

# Given a username, password, label, and mailserver, log in and get/manage
# emails

class MailReader:
    def __init__(self, username, password, label, server):
        self.imap = imaplib.IMAP4_SSL(server, timeout=10)
        self.imap.login(username, password)
        # the mailbox to pull from
        self.label = label

    # returns list of mail subjects that are unread
    def readUnreadMailSubjects(self):
        # returns number of emails in the box as (status, [num_mails])
        self.imap.select(mailbox=self.label)

        # Returns space sep string, in a list of matching mail id's 
        # (status, [ids_str])
        status, ids_str = self.imap.search(None, 'UNSEEN')
        ids = messages[0].split()

        subjects = set()
        for email_id in ids:
            # (typ, [data, ...])
            # 'data' are tuples of message part envelope and data.
            status, data = mail.fetch(email_id, '(RFC822)')
            raw_data = msg_data[0][1]
            msg = email.message_from_bytes(raw_data)
            subject, encoding = decode_header(msg['Subject'])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or 'utf-8')
            subjects.append(subject)
