import asyncio
from ApiAccess import ApiAccess
from UserRequest import UserRequest
import argparse
import threading
import json
import parser
import time



def parse_console_input():
    """
    Responsible for parsing the console
    arguments that is provided by user.
    It accepts a mode, input type and optionally
    expend the details of output and write into a file
    or print out.
    :return: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("side", help="{Buy | Sell}")
    parser.add_argument("size", type=int, help="Size of the contract")
    parser.add_argument("interval", type=int, help="Time interval: how often a trade signal will"
                                         "be sent")
    parser.add_argument("tp", type=int, help="Take profit")
    parser.add_argument("sl", type=int, help='Stop loss')
    args = parser.parse_args()
    side = ''
    size = 0
    interval = 0
    tp = 0
    sl = 0

    try:
        side = args.side
        size = args.size
        interval = args.interval
        tp = args.tp
        sl = args.sl
    except Exception as e:
        print(f"Error! Could not read arguments. \n{e}")
        quit()

    return UserRequest(side,size,interval,tp,sl)

class Trader:
    def __init__(self, access, ur):
        self.access = access
        self.ur = ur
        self.order_id_buy = None
        self.order_id_sell = None
        self.active_size = ur.contract_size
        self.tp = ur.get_tp()

    async def first_trade(self, new_size=None, new_side=None, tp=None):
        data = await access.access_order_book()
        buy_sell = access.highest_buy_lowest_sell(data)
        if new_size is not None:
            size = new_size
        else:
            size = ur.contract_size
        if new_side is not None:
            side = new_side
        else:
            side = ur.get_side()


        symbol = 'BTCUSD'
        price = 0
        if side == 'Buy':
            price = float(buy_sell[0])
        elif side == 'Sell':
            price = float(buy_sell[0])
            if tp is not None:
                price = price + float(tp)
        order_data = await access.place_order(side, symbol, price, size)
        order_data = order_data["result"]
        if new_side is not None:
            self.order_id_sell = order_data["order_id"]
        self.order_id_buy = order_data["order_id"]


    def start_trade(self):
        threading.Timer(ur.time_interval, self.start_trade).start()
        data = asyncio.run(access.access_position())
        size = data["result"][0]["size"]
        if size == 0:
            asyncio.run(access.cancel_order('BTCUSD', self.order_id_buy))
            asyncio.run(self.first_trade())
        else:
            if self.order_id_buy is not None:
                asyncio.run(access.cancel_order('BTCUSD', self.order_id_buy))
            if self.order_id_sell is not None:
                asyncio.run(access.cancel_order('BTCUSD', self.order_id_sell))
            print("Something executed!")
            asyncio.run(self.first_trade(new_size=size,new_side='Sell', tp=self.tp))
            asyncio.run(self.first_trade())






if __name__ == "__main__":
    ur = parse_console_input()
    access = ApiAccess()
    trader = Trader(access,ur)
    asyncio.run(trader.first_trade())
    time.sleep(ur.time_interval)
    trader.start_trade()






    # asyncio.run(access.set_leverage('BTCUSD', 1))
    # asyncio.run(access.set_leverage('EOSUSD', 1))
    # asyncio.run(access.set_leverage('ETHUSD', 1))
    # asyncio.run(access.set_leverage('XRPUSD', 1))
    # print(asyncio.run(access.access_leverage()))