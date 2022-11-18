from mongoengine import *
import uuid

class Ticker(Document):
    id = UUIDField()
    candle_stick_id = UUIDField()
    timestamp = DateTimeField()
    symbol = StringField()
    interval = StringField()
    
    def _init__(self, candle_stick_id, symbol, timestamp, interval):
        self.ticker_id = uuid.uuid4
        self.candle_stick_id = candle_stick_id
        self.symbol = symbol
        self.timestamp = timestamp
        self.interval = interval