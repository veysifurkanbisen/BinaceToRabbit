from mongoengine import *

def add_new_candle_stick(app, candle_stick):
    
    add_new_candle_stick = app.database["CandleStick"].insert_one(candle_stick)
    created_candle_stick_id = add_new_candle_stick.inserted_id
    return created_candle_stick_id

def add_new_ticker(ticker):
    pass