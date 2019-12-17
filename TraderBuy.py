import asyncio
import threading

class TraderBuy:
    def __init__(self, access, ur):
        self.access = access
        self.ur = ur
        self.order_id_buy = None
        self.order_id_sell = None
        self.active_size = ur.contract_size
        self.tp = ur.get_tp()

    async def trade(self, new_size=None, new_side=None, tp=None):
        """
        Trades with 2 modes.
        If parameters are not given, their default value is None
        and trades constructed with original input
        if parameters are given, they will be send
        :param new_size: size of the contract
        :param new_side: side of the trade
        :param tp: final tp value to send
        :return:
        """
        data = await self.access.access_order_book()
        buy_sell = self.access.highest_buy_lowest_sell(data)

        if new_size is not None:
            size = new_size
        else:
            size = self.ur.contract_size
        if new_side is not None:
            side = new_side
        else:
            side = self.ur.get_side()

        symbol = 'BTCUSD'
        price = 0
        if side == 'Buy':
            price = float(buy_sell[0])
        elif side == 'Sell':
            price = float(buy_sell[0])
            if tp is not None:
                price = tp
                if price < float(buy_sell[0]):
                    price = buy_sell[0]

        order_data = await self.access.place_order(side, symbol, price, size)
        order_data = order_data["result"]
        if new_side is not None:
            self.order_id_sell = order_data["order_id"]
        else:
            self.order_id_buy = order_data["order_id"]


    def start_trade(self):
        """
        Starts the trading sequence. Interval is provided by User
        makes decisions on which side to place order, cleaning orders
        and placing them
        :return:
        """
        threading.Timer(self.ur.time_interval, self.start_trade).start()

        data = asyncio.run(self.access.access_position())
        try:
            size = data["result"][0]["size"]
            tp_price = data["result"][0]["entry_price"]
            tp_price = float(tp_price) + self.tp
            print("Get data: average tp: ",tp_price)
        except TypeError as e:
            print("Type error setting size to 0")
            size = 0
        if size == 0:
            asyncio.run(self.access.cancel_order('BTCUSD', self.order_id_buy))
            asyncio.run(self.trade())
        else:
            if self.order_id_buy is not None:
                asyncio.run(self.access.cancel_order('BTCUSD', self.order_id_buy))
            if self.order_id_sell is not None:
                asyncio.run(self.access.cancel_order('BTCUSD', self.order_id_sell))
            print("Something executed!")
            asyncio.run(self.trade(new_size=size, new_side='Sell', tp=tp_price))
            asyncio.run(self.trade())

    async def remove_all_first(self):
        await self.access.cancel_all_orders("BTCUSD")