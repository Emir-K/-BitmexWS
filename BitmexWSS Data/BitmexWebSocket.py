import asyncio
import websockets
import json
from main import FileHandler


url = "wss://www.bitmex.com/realtime"



async def bitmex_ws():
    fs = FileHandler()
    params = '{"op": "subscribe", "args": ["liquidation:XBTUSD", "funding:XBTUSD", "trade:XBTUSD", "connected", ' \
             '"tradeBin1m:XBTUSD", "tradeBin5m:XBTUSD", "tradeBin1h:XBTUSD", "tradeBin1d:XBTUSD"]}'
    async with websockets.connect(url) as websocket:
        await websocket.send(params)

        async for message in websocket:
            data = json.loads(message)
            try:

                if data["table"] == "trade":
                    data_list = data["data"]
                    for item in data_list:
                        if int(item["size"] > 100000):
                            if item["side"] == "Buy":
                                fs.write_long_orders_data(item)
                            else:
                                fs.write_short_orders_data(item)

                elif data["table"] == "liquidation":
                    data_list = data["data"]
                    for item in data_list:
                        if int(item["leavesQty"] > 100000):
                            if item["side"] == "Buy":
                                fs.write_long_liq_data(item)
                            else:
                                fs.write_short_liq_data(item)
                else:
                    if data["table"] == "funding":
                        fs.write_funding_data(message)

                    elif data["table"] == "connected":
                        fs.write_connected_data(message)

                    elif data["table"] == "tradeBin1m":
                        fs.write_one_min_trade_data(message)

                    elif data["table"] == "tradeBin5m":
                        fs.write_five_min_trade_data(message)

                    elif data["table"] == "tradeBin1h":
                        fs.write_one_hour_trade_data(message)

                    elif data["table"] == "tradeBin1d":
                        fs.write_one_day_trade_data(message)

            except Exception as e:
                print(e)
                pass






if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(bitmex_ws())
    asyncio.get_event_loop().run_forever()