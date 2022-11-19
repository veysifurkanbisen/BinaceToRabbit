import requests
# import json
# from dotenv import load_dotenv, dotenv_values
# import os
# from pathlib import Path
import datetime

# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path = env_path)
# config = dotenv_values(".env")
uri = "https://api.binance.com"
path = "/api/v3/klines"

paramters = {
    "symbol": 'symbol=',
    "interval": 'interval=',
    "startTime": 'startTime=',
    "endTime": 'endTime='
}

class Binance():
    
    def _init__(self, symbol: str, interval: str, startTime: datetime = None, endTime:datetime = None):
        self.symbol = symbol
        self.interval = interval
        self.startTime = startTime
        self.endTime = endTime

    def get_binance_data(self):
        url = uri + path + '?' + paramters["symbol"] + self.symbol + '&' + paramters["interval"] + self.interval

        if self.startTime is not None:
            url += '&' + paramters["startTime"] + str(self.startTime)
        if self.endTime is not None:
            url += '&' + paramters["endTime"] + str(self.endTime)

        data = requests.get(url).json()
        print("data", data, "\n" + url)

        return data