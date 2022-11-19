import time as Time
import datetime
from Services.binance_service import Binance
from Services.db_service import add_new_candle_stick as SaveCandleStick
from Services.db_service import add_new_ticker as SaveTicker
from Services import db_service
from Services.queue_service import UserQueue
from Models.CandleStickModel import CandleStick
from Models.TickerModel import Ticker


current_user_options = {
    "symbol": "BTCUSDT",
    "interval": "1h"
}

database_record_intervals = {
    "interval_1": "1m",
    "interval_2": "15m",
    "interval_3": "1h",
    "interval_4": "4h",
    "interval_5": "1d"

}


def work(app):
    while True:
        # CHECK TIME FOR INTERVAL
        time = get_time()
        interval = 0
        today = datetime.datetime.utcnow()
        tomorrow = today + datetime.timedelta(days=1)
        # print(today.timestamp() * 1000, "\n" , tomorrow.timestamp())

        # Save To Database
        if time == database_record_intervals["interval_1"]:
            # Feed Queue
            if len(UserQueue.users) > 0:
                pass
            pass
        if time == database_record_intervals["interval_2"]:
            pass
        if time == database_record_intervals["interval_3"]:
            pass
        if time == database_record_intervals["interval_4"]:
            pass
        if time == database_record_intervals["interval_5"]:
            pass


        # candle_sticks = generate_binance_object(current_user_options["symbol"], current_user_options["interval"], today, tomorrow)
        # save_candle_stick_and_ticker(app, candle_sticks, symbol, interval)
        # Time.sleep(5)

def get_time():
    return 0

def generate_binance_object(symbol, interval, start_date, end_date):
    binance = Binance()
    binance.symbol = symbol
    binance.interval = interval
    binance.startTime = int(start_date.timestamp())*1000
    binance.endTime = int(end_date.timestamp())*1000

    data = binance.get_binance_data()

    # print(data)
    return data
        
def save_candle_stick_and_ticker(app, candleSticks, symbol, interval):
    print(candleSticks)
    
    for candleStick in candleSticks:

        tickerModel = Ticker()
        tickerModel.interval = interval
        tickerModel.symbol = symbol

        is_ticker_exists = db_service.check_if_ticker_exists(app, tickerModel)
        if is_ticker_exists:
            ticker_id = db_service.get_ticker_id(app, tickerModel)
        else:
            ticker_id = SaveTicker(app, tickerModel)


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
        # print(id)


    
    return None


def feed_queue(user_name, symbol, interval, candle_stick):

    return
    
