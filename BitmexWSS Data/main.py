import asyncio
import aiohttp
import json


url = 'https://www.bitmex.com/api/v1/liquidation?count=100'
url_funding = "https://www.bitmex.com/api/v1/funding?count=100&reverse=true"


class FileHandler:
    def __init__(self):
        self.long_liq_file_path = "long_liq.txt_data.txt"
        self.short_liq_file_path = "short_liq.txt_data.txt"
        self.funding_file_path = "historic_funding_rate.txt"
        self.long_orders_file_path = "long_orders.txt_data.txt"
        self.short_orders_file_path = "short_orders.txt_data.txt"
        self.connected_file_path = "connected_data.txt"
        self.one_min_trade_file_path = "1min_trade_data.txt"
        self.five_min_trade_file_path = "5min_trade_data.txt"
        self.one_hour_trade_file_path = "1hour_trade_data.txt"
        self.one_day_trade_file_path = "1day_trade_data.txt"

    def write_long_liq_data(self, data):
        with open( self.long_liq_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_short_liq_data(self, data):
        with open(self.short_liq_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_funding_data(self, data):
        with open(self.funding_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_long_orders_data(self, data):
        with open(self.long_orders_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_short_orders_data(self, data):
        with open(self.short_orders_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_connected_data(self, data):
        with open(self.connected_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_one_min_trade_data(self, data):
        with open(self.one_min_trade_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_five_min_trade_data(self, data):
        with open(self.five_min_trade_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_one_hour_trade_data(self, data):
        with open(self.one_hour_trade_file_path, "a") as file:
            file.write(f"{data}\n")

    def write_one_day_trade_data(self, data):
        with open(self.one_day_trade_file_path, "a") as file:
            file.write(f"{data}\n")





if __name__ == '__main__':
    fs = FileHandler()
    fs.write_funding_data("Hello")
   # liq = asyncio.run(get_liq())
   # funding = asyncio.run(get_funding())
   # parsed_funding = []
   # for item in funding:
   #      symbol = item["symbol"]
   #      if symbol == "XBTUSD":
   #          parsed_funding.append(item)
   #
   # fileHandle_liq(liq)
   # fileHandle_funding(parsed_funding)
    # data = asyncio.run(get_latest())
    # print(data)
    # print(dat)
    # fileHandle(data)