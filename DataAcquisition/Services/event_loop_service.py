import time as Time
import datetime
import schedule
from Services.binance_service import Binance
from Services.db_service import add_new_candle_stick as SaveCandleStick
from Services.db_service import add_new_ticker as SaveTicker
from Services import db_service
from Services.queue_service import UserQueue
from Models.CandleStickModel import CandleStick
from Models.TickerModel import Ticker


current_user_options = {
    "symbol": "BTCUSDT",
    "interval": "1d"
}

intervals = {
    "interval_1": "1m",
    "interval_2": "15m",
    "interval_3": "1h",
    "interval_4": "4h",
    "interval_5": "1d",
}

def work(app):
    # Save To DB
    schedule.every().minute.at(":00").do(interval_job_1m, app=app, symbol=current_user_options["symbol"], interval=intervals["interval_1"])
    schedule.every().minute.at(":00").do(interval_job_15m, app=app, symbol=current_user_options["symbol"], interval=intervals["interval_2"])
    schedule.every().hour.at("00:00").do(interval_job_1h, app=app, symbol=current_user_options["symbol"], interval=intervals["interval_3"])
    schedule.every().hour.at("00:00").do(interval_job_4h, app=app, symbol=current_user_options["symbol"], interval=intervals["interval_4"])
    schedule.every().day.at("00:00:00").do(interval_job_1d, app=app, symbol=current_user_options["symbol"], interval=intervals["interval_5"])

    while True:
        schedule.run_pending()

def interval_job_1m(app, symbol, interval):
    print(interval)
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(minutes=1)

    available_times = [0, 15,16, 17, 18, 19, 30, 45]
    if time.minute in available_times:
        print("AAAAAAAAAAAAAAAAAAAAAAAA")


    candle_sticks = generate_binance_object(symbol, interval, before, now)
    save_candle_stick_and_ticker(app, candle_sticks, symbol, interval)

def interval_job_15m(app, symbol, interval):
    print(interval)
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(minutes=15)

    available_times = [0, 15, 30, 45]
    if time.minute in available_times:
        candle_sticks = generate_binance_object(symbol, interval, before, now)
        save_candle_stick_and_ticker(app, candle_sticks, symbol, interval)

def interval_job_1h(app, symbol, interval):
    print(interval)
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(hours=1)

    candle_sticks = generate_binance_object(symbol, interval, before, now)
    save_candle_stick_and_ticker(app, candle_sticks, symbol, interval)

def interval_job_4h(app, symbol, interval):
    print(interval)
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(hours=4)
    
    available_times = [0, 4, 8, 12, 16, 20]
    if time.hour in available_times:
        candle_sticks = generate_binance_object(symbol, interval, before, now)
        save_candle_stick_and_ticker(app, candle_sticks, symbol, interval)
    
def interval_job_1d(app,  symbol, interval):
    print(interval)
    time = datetime.datetime.utcnow().replace(microsecond=0)
    now = time
    before = time - datetime.timedelta(days=1)

    candle_sticks = generate_binance_object(symbol, interval, before, now)
    save_candle_stick_and_ticker(app, candle_sticks, symbol, interval)

def generate_binance_object(symbol, interval, start_date, end_date):
    print(start_date, "-", end_date)
    binance = Binance()
    binance.symbol = symbol
    binance.interval = interval
    binance.startTime = int(start_date.timestamp()) * 1000
    binance.endTime = int(end_date.timestamp()) * 1000

    data = binance.get_binance_data()

    return data
        
def save_candle_stick_and_ticker(app, candleSticks, symbol, interval):
    print("Saving...")
    for candleStick in candleSticks:
        print("candleStick", candleStick)
        tickerModel = Ticker()
        tickerModel.timestamp = str(datetime.datetime.utcnow())
        tickerModel.interval = interval
        tickerModel.symbol = symbol

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

        candle_stick_id = SaveCandleStick(app, candleStickModel.to_mongo())


def feed_queue():
    # Feed User Queues
    for user in UserQueue.eixsting_users:
        print (user)


    while True:
        print("feed_queue")
        Time.sleep(1)
    
