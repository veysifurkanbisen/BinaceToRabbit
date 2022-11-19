from mongoengine import *
import uuid

class CandleStick(Document):
    id = UUIDField()
    ticker_id = UUIDField()
    timestamp = DateTimeField()
    length = StringField()
    high = StringField()
    low = StringField()
    open = StringField()
    close = StringField()
    volume = StringField()
    open_time = StringField()
    close_time = StringField()
    quote_asset_volume = StringField()
    trade_number = StringField()

    def _init__(self, timestamp, ticker_id, length, high, low, open, close , volume, open_time, close_time, quote_asset_volume, trade_number):
        self.candle_stick_id = uuid.uuid4
        self.timestamp = timestamp
        self.ticker_id = ticker_id
        self.length = length
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume
        self.open_time = open_time
        self.close_time = close_time
        self.quote_asset_volume = quote_asset_volume
        self.trade_number = trade_number