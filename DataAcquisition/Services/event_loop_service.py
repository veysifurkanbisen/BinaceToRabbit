import time
import datetime
from Services.binance_service import Binance
from Services.db_service import add_new_candle_stick as SaveCandleStick
from Services.db_service import add_new_ticker as SaveTicker
from Models.CandleStickModel import CandleStick


current_user_options = {
    "symbol": "BTCUSDT",
    "interval": "1h"
}

def work(app):
    while True:
        today = datetime.datetime.utcnow()
        tomorrow = today + datetime.timedelta(days=1)
        # print(today.timestamp() * 1000, "\n" , tomorrow.timestamp())

        candle_sticks = generate_binance_object(current_user_options["symbol"], current_user_options["interval"], today, tomorrow)
        save_candle_stick_and_ticker(app, candle_sticks)
        time.sleep(5)

def generate_binance_object(symbol, interval, start_date, end_date):
    binance = Binance()
    binance.symbol = symbol
    binance.interval = interval
    binance.startTime = int(start_date.timestamp())*1000
    binance.endTime = int(end_date.timestamp())*1000

    data = binance.get_binance_data()

    # print(data)
    return data
        
def save_candle_stick_and_ticker(app, candleSticks):
    print(candleSticks)
    
    for candleStick in candleSticks:
        candleStickModel = CandleStick()
        
        candleStickModel.timestamp = str(datetime.datetime.utcnow())
        candleStickModel.open_time = str(candleStick[0])
        candleStickModel.open = str(candleStick[1])
        candleStickModel.high = str(candleStick[2])
        candleStickModel.low = str(candleStick[3])
        candleStickModel.close = str(candleStick[4])
        candleStickModel.volume = str(candleStick[5])
        candleStickModel.close_time = str(candleStick[6])
        candleStickModel.quote_asset_volume = str(candleStick[7])
        candleStickModel.trade_number = str(candleStick[8])

        # id = SaveCandleStick(app, candleStickModel.to_mongo())
        # print(id)
    
    

    return None


def feed_queue(user_name, symbol, interval, candle_stick):
    return
    
