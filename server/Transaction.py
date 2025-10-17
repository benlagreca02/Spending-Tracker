import hashlib
from zoneinfo import ZoneInfo

class Transaction:
    def __init__(self, amount, merchant, timestamp, local_timezone=ZoneInfo("UTC")):
        self.amount = amount
        self.merchant = merchant
        self.timestamp = timestamp
        self.id = None
        self.local_timezone = local_timezone
 
    def __str__(self):
        # "Mon Jan 2022, 11:59PM" for example
        timestampLocalized = self.timestamp.astimezone(self.local_timezone)
        dateFormatted = timestampLocalized.strftime('%a %d %b %Y, %I:%M%p')
        return f"${self.amount} spent at {self.merchant} on {dateFormatted} {self.local_timezone}"

    def __repr__(self):
        return f"${self.amount}-{self.merchant}-{self.timestamp}"

    def get_id(self):
        if self.id is None:
            self.id = hashlib.sha256(self.__repr__().encode()).hexdigest()
        return self.id
