from mongoengine import *

def add_new_candle_stick(app, candle_stick):
    
    add_new_candle_stick = app.database["CandleStick"].insert_one(candle_stick)
    created_candle_stick_id = add_new_candle_stick.inserted_id
    return created_candle_stick_id

def add_new_ticker(app, ticker):
    
    add_new_ticker = app.database["Ticker"].insert_one(ticker)
    created_ticker_id = add_new_ticker.inserted_id
    return created_ticker_id

def check_if_ticker_exists(app, ticker):
    is_exists = app.database["Ticker"].find(ticker).count() > 0
    return is_exists

def get_ticker_id(app, ticker):
    ticker_doc = app.database["Ticker"].find_one(ticker)
    ticker_id = ticker_doc.get('_id')
    return ticker_id