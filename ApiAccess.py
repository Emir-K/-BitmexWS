import hmac
from datetime import timezone, datetime
import aiohttp

class ApiAccess:
    def __init__(self):
        self.base = 'https://api-testnet.bybit.com'
        self._api_key = "IP0ZIgda9ycQ2avsKV"
        self._secret = "errFTCXME5k91D0wxqa3ouqS5BClM7ECkAel"

    @staticmethod
    def get_signature(secret: str, req_params: dict):
        """
        :param secret    : str, your api-secret
        :param req_params: dict, your request params
        :return: signature
        """
        _val = '&'.join([str(k)+"="+str(v) for k, v in sorted(req_params.items()) if (k != 'sign') and (v is not None)])
        return str(hmac.new(bytes(secret, "utf-8"), bytes(_val, "utf-8"), digestmod="sha256").hexdigest())

    @staticmethod
    def utc_now():
        return int(datetime.now(tz=timezone.utc).timestamp() * 1000)

    async def get_order_book(self, base, queryParams):
        async with aiohttp.ClientSession() as session:
            query = f'{base}{queryParams["position"]}?symbol={queryParams["symbol"]}'
            response = await session.get(url=query)
            return await response.json()

    async def access_order_book(self):
        params = {}
        params['position'] = '/v2/public/orderBook/L2'
        params['symbol'] = 'BTCUSD'
        data =  await self.get_order_book(self.base, params)
        return data

    async def get_leverage(self, base, queryParams):
        async with aiohttp.ClientSession() as session:
            query = f'{base}{queryParams["fund"]}?api_key={self._api_key}' \
                    f'&timestamp={queryParams["timestamp"]}' \
                    f'&sign={queryParams["sign"]}'
            response = await session.get(url=query)
            return await response.json()

    async def access_leverage(self):
        params = {}
        params['api_key'] = self._api_key
        params['timestamp'] = self.utc_now()
        sign  = self.get_signature(self._secret, params)
        params['sign'] = sign
        params['fund'] = '/user/leverage'
        data = await self.get_leverage(self.base, params)
        return data

    def highest_buy_lowest_sell(self, data):
        highest_buy = data["result"][0]['price']
        lowest_sell = data["result"][25]['price']
        return [highest_buy, lowest_sell]

    async def post_leverage(self, queryParams):
        async with aiohttp.ClientSession() as session:
            query = f'{self.base}{queryParams["root"]}?api_key={self._api_key}' \
                    f'&leverage={queryParams["leverage"]}&symbol={queryParams["symbol"]}'\
                    f'&timestamp={queryParams["timestamp"]}' \
                    f'&sign={queryParams["sign"]}'
            response = await session.post(url=query)
            return await response.json()

    async def set_leverage(self, symbol, leverage):
        params = {}
        params['api_key'] = self._api_key
        params['timestamp'] = self.utc_now()
        params['symbol'] = symbol
        params['leverage'] = leverage
        sign = self.get_signature(self._secret, params)
        params['sign'] = sign
        params['root'] = '/user/leverage/save'
        res = await self.post_leverage(params)
        return res

    async def place_order(self, side, symbol, price, quantity):
        params = {}
        params['api_key'] = self._api_key
        params['timestamp'] = self.utc_now()
        params['side'] = side
        params['symbol'] = symbol
        params['order_type'] = 'Limit'
        params['qty'] = quantity
        params['price'] = price
        params['time_in_force'] = 'GoodTillCancel'
        # params['take_profit'] = tp
        # params['reduce_only'] = 'true'
        sign = self.get_signature(self._secret, params)
        params['sign'] = sign
        params['root'] = '/v2/private/order/create'
        res = await self.post_trade(params)
        return res

    async def post_trade(self,queryParams):
        async with aiohttp.ClientSession() as session:
            query = f'{self.base}{queryParams["root"]}?api_key={self._api_key}' \
                    f'&side={queryParams["side"]}&symbol={queryParams["symbol"]}'\
                    f'&order_type={queryParams["order_type"]}&qty={queryParams["qty"]}' \
                    f'&price={queryParams["price"]}&time_in_force={queryParams["time_in_force"]}' \
                    f'&timestamp={queryParams["timestamp"]}' \
                    f'&sign={queryParams["sign"]}'
            response = await session.post(url=query)
            return await response.json()

    async def get_position(self, queryParams):
        async with aiohttp.ClientSession() as session:
            query = f'{self.base}{queryParams["root"]}?api_key={self._api_key}' \
                    f'&timestamp={queryParams["timestamp"]}' \
                    f'&sign={queryParams["sign"]}'
            response = await session.get(url=query)
            return await response.json()

    async def access_position(self):
        params = {}
        params['api_key'] = self._api_key
        params['timestamp'] = self.utc_now()
        sign = self.get_signature(self._secret, params)
        params['root'] = '/position/list'
        params['sign'] = sign
        data = await self.get_position(queryParams=params)
        return data


    async def remove(self, queryParams):
        async with aiohttp.ClientSession() as session:
            query = f'{self.base}{queryParams["root"]}?api_key={self._api_key}' \
                    f'&symbol={queryParams["symbol"]}'\
                    f'&order_id={queryParams["order_id"]}' \
                    f'&timestamp={queryParams["timestamp"]}' \
                    f'&sign={queryParams["sign"]}'
            response = await session.post(url=query)
            return await response.json()

    async def cancel_order(self, symbol, order_id):
        params ={}
        params['api_key'] = self._api_key
        params['timestamp'] = self.utc_now()
        params['symbol'] = symbol
        params['order_id'] = order_id
        sign = self.get_signature(self._secret, params)
        params['root'] = '/v2/private/order/cancel'
        params['sign'] = sign
        return await self.remove(queryParams=params)