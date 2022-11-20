from mongoengine import *
import uuid

class Ticker(Document):
    id = UUIDField()
    timestamp = DateTimeField()
    symbol = StringField()
    interval = StringField()
    
    def _init__(self, symbol, timestamp, interval):
        self.ticker_id = uuid.uuid4
        self.symbol = symbol
        self.timestamp = timestamp
        self.interval = interval