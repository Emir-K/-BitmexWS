import asyncio
import threading
import time


class TraderBuy:
    def __init__(self, access, ur):
        self.access = access
        self.ur = ur
        self.order_id_buy = None
        self.order_id_sell = None
        self.active_size = ur.contract_size
        self.tp = ur.get_tp()

    async def trade(self, new_size=None, new_side=None, new_tp=None):
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
        data = await self.access.latest_info()
    #         Get order book data and fetch the highest high and lowest low.
        buy_sell = self.access.highest_buy_lowest_sell(data)

        """
        If params are provided use them to update the trade
        parameters.
        """

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
            if self.ur.double_size > float(buy_sell[2]):
                size  = size * 2
            price = float(buy_sell[0])
        elif side == 'Sell':
            price = float(buy_sell[1])
            if new_tp is not None:
                price = new_tp
                if price < float(buy_sell[1]):
                    price = buy_sell[1]


        await self.access.place_order(side, symbol, price, size)

    def start_trade(self):
        """
        Starts the trading sequence. Interval is provided by User
        makes decisions on which side to place order, cleaning orders
        and placing them
        :return:
        """
        threading.Timer(self.ur.time_interval, self.start_trade).start()
        asyncio.run(self.remove_all_first())
        if not self.ur.limit:
            asyncio.run(self.trade())
        time.sleep(3)
        data = asyncio.run(self.access.access_position())
        try:
            size = data["result"][0]["size"]
        except TypeError as e:
            size = 0
        if self.ur.max_size < size:
            self.ur.limit = True
        else:
            self.ur.limit = False
        if size != 0:
            tp_price = data["result"][0]["entry_price"]
            tp_price = float(tp_price) + self.tp
            asyncio.run(self.trade(new_size=size, new_side='Sell', new_tp=tp_price))


    async def remove_all_first(self):
        await self.access.cancel_all_orders("BTCUSD")