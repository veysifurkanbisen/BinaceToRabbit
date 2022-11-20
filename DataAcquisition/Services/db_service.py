from mongoengine import *

def add_new_candle_stick(app, candle_stick):
    print("inserted CandleStick")
    add_new_candle_stick = app.database["CandleStick"].insert_one(candle_stick)
    created_candle_stick_id = add_new_candle_stick.inserted_id

    return created_candle_stick_id

def add_new_ticker(app, ticker):
    print("inserted Ticker")
    add_new_ticker = app.database["Ticker"].insert_one(ticker)
    created_ticker_id = add_new_ticker.inserted_id
    return created_ticker_id


def get_ticker_id(app, interval, symbol):
    try:
        ticker_doc = app.database["Ticker"].find({"interval": interval, "symbol": symbol})[0]
        ticker_id = ticker_doc.get('_id')
        return ticker_id
    except:
        return None
        