import time as Time
import datetime
import schedule
from Services.binance_service import Binance
from Services.db_service import add_new_candle_stick as SaveCandleStick
from Services.db_service import add_new_ticker as SaveTicker
from Services import db_service
from Utils import json_util
from Services.queue_service import UserQueue
from Models.CandleStickModel import CandleStick
from Models.TickerModel import Ticker
from dotenv import dotenv_values

config = dotenv_values()

def work(app):
    # Save To DB
    schedule.every().minute.at(":00").do(interval_job_1m, app=app, symbol=config["Symbol"], interval=config["Interval_1"], is_queue=False)
    schedule.every().minute.at(":00").do(interval_job_15m, app=app, symbol=config["Symbol"], interval=config["Interval_2"], is_queue=False)
    schedule.every().hour.at("00:00").do(interval_job_1h, app=app, symbol=config["Symbol"], interval=config["Interval_3"], is_queue=False)
    schedule.every().hour.at("00:00").do(interval_job_4h, app=app, symbol=config["Symbol"], interval=config["Interval_4"], is_queue=False)
    schedule.every().day.at("00:00:00").do(interval_job_1d, app=app, symbol=config["Symbol"], interval=config["Interval_5"], is_queue=False)

    while True:
        schedule.run_pending()

def interval_job_1m(app, symbol, interval, is_queue):

    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(minutes=1)

    candle_sticks = generate_binance_object(symbol, interval, before, now)
    result = save_candle_stick_and_ticker(app, candle_sticks, symbol, interval, is_queue)
    return result

def interval_job_15m(app, symbol, interval, is_queue):
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(minutes=15)

    available_times = [0, 15, 30, 45]
    if time.minute in available_times or is_queue:
        candle_sticks = generate_binance_object(symbol, interval, before, now)
        result = save_candle_stick_and_ticker(app, candle_sticks, symbol, interval, is_queue)
        return result

def interval_job_1h(app, symbol, interval, is_queue):
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(hours=1)

    candle_sticks = generate_binance_object(symbol, interval, before, now)
    result = save_candle_stick_and_ticker(app, candle_sticks, symbol, interval, is_queue)
    return result

def interval_job_4h(app, symbol, interval, is_queue):
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(hours=4)
    
    available_times = [0, 4, 8, 12, 16, 20]
    if time.hour in available_times or is_queue:
        candle_sticks = generate_binance_object(symbol, interval, before, now)
        result = save_candle_stick_and_ticker(app, candle_sticks, symbol, interval, is_queue)
        return result
    
def interval_job_1d(app, symbol, interval, is_queue):
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(days=1)

    candle_sticks = generate_binance_object(symbol, interval, before, now)
    result = save_candle_stick_and_ticker(app, candle_sticks, symbol, interval, is_queue)
    return result

def generate_binance_object(symbol, interval, start_date, end_date):
    binance = Binance()
    binance.symbol = symbol
    binance.interval = interval
    binance.startTime = int(start_date.timestamp()) * 1000
    binance.endTime = int(end_date.timestamp()) * 1000

    data = binance.get_binance_data()

    return data
        
def save_candle_stick_and_ticker(app, candleSticks, symbol, interval, is_queue = False):
    for candleStick in candleSticks:
        tickerModel = Ticker()
        tickerModel.timestamp = str(datetime.datetime.utcnow())
        tickerModel.interval = interval
        tickerModel.symbol = symbol
        
        ticker_id = 0
        if not is_queue:
            # print("Saving...")
            ticker_id = db_service.get_ticker_id(app, interval, symbol)
        if ticker_id == None:
            ticker_id = SaveTicker(app, tickerModel.to_mongo())

        candleStickModel = CandleStick()
        candleStickModel.timestamp = str(datetime.datetime.utcnow())
        candleStickModel.ticker_id = ticker_id
        candleStickModel.open_time = str(candleStick[0])
        candleStickModel.open = str(candleStick[1])
        candleStickModel.high = str(candleStick[2])
        candleStickModel.low = str(candleStick[3])
        candleStickModel.close = str(candleStick[4])
        candleStickModel.volume = str(candleStick[5])
        candleStickModel.close_time = str(candleStick[6])
        candleStickModel.quote_asset_volume = str(candleStick[7])
        candleStickModel.trade_number = str(candleStick[8])
        
        if not is_queue:
            # print("Saving...")
            candle_stick_id = SaveCandleStick(app, candleStickModel.to_mongo())
    
    result = {
        "CandleStick": candleStickModel.to_json(),
        "Ticker": tickerModel.to_json()
    }
    return result

def feed_queue(app):
    # Feed User Queues
    while True:
        print("Sending Queue...")
        user_list = json_util.read_json()
        for user in user_list:            
            interval_1_queue = user["user_name"] + "." + user["symbol"] + "." + config["Interval_1"]
            interval_2_queue = user["user_name"] + "." + user["symbol"] + "." + config["Interval_2"]
            interval_3_queue = user["user_name"] + "." + user["symbol"] + "." + config["Interval_3"]
            interval_4_queue = user["user_name"] + "." + user["symbol"] + "." + config["Interval_4"]
            interval_5_queue = user["user_name"] + "." + user["symbol"] + "." + config["Interval_5"]

            interval_1_message = interval_job_1m(app, user["symbol"], config["Interval_1"], is_queue=True)
            interval_2_message = interval_job_15m(app, user["symbol"], config["Interval_2"], is_queue=True)
            interval_3_message = interval_job_1h(app, user["symbol"], config["Interval_3"], is_queue=True)
            interval_4_message = interval_job_4h(app, user["symbol"], config["Interval_4"], is_queue=True)
            interval_5_message = interval_job_1d(app, user["symbol"], config["Interval_5"], is_queue=True)

            UserQueue(user["user_name"], user["symbol"]).feed_queues(interval_1_message, interval_1_queue)
            UserQueue(user["user_name"], user["symbol"]).feed_queues(interval_2_message, interval_2_queue)
            UserQueue(user["user_name"], user["symbol"]).feed_queues(interval_3_message, interval_3_queue)
            UserQueue(user["user_name"], user["symbol"]).feed_queues(interval_4_message, interval_4_queue)
            UserQueue(user["user_name"], user["symbol"]).feed_queues(interval_5_message, interval_5_queue)

        Time.sleep(int(config["Frequency"]))
    
