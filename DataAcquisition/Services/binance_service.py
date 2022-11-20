import requests
# import json
# from dotenv import load_dotenv, dotenv_values
# import os
# from pathlib import Path
import datetime
from dotenv import dotenv_values

config = dotenv_values()

class Binance():
    
    def _init__(self, symbol: str, interval: str, startTime: datetime = None, endTime:datetime = None):
        self.symbol = symbol
        self.interval = interval
        self.startTime = startTime
        self.endTime = endTime

    def get_binance_data(self):
        url = config["Binance_URI"] + config["Binance_Path"] + '?' + config["Binance_Params_Symbol"] + self.symbol + '&' + config["Binance_Params_Interval"] + self.interval

        if self.startTime is not None:
            url += '&' + config["Binance_Params_StartTime"] + str(self.startTime)
        if self.endTime is not None:
            url += '&' + config["Binance_Params_EndTime"] + str(self.endTime)

        data = requests.get(url).json()
        return data