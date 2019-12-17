from TraderBuy import TraderBuy
from UserRequest import UserRequest
from SellAccess import ApiAccessSell
from BuyAccess import ApiAccessBuy
from TraderSell import TraderSell
import argparse
import asyncio
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


if __name__ == "__main__":
    ur = parse_console_input()
    trader = None
    if ur.get_side() == 'Buy':
        access = ApiAccessBuy()
        trader = TraderBuy(access, ur)
    elif ur.get_side() == 'Sell':
        access = ApiAccessSell()
        trader = TraderSell(access, ur)
    asyncio.run(trader.remove_all_first())
    asyncio.run(trader.trade())
    time.sleep(ur.time_interval)
    trader.start_trade()






    # asyncio.run(access.set_leverage('BTCUSD', 1))
    # asyncio.run(access.set_leverage('EOSUSD', 1))
    # asyncio.run(access.set_leverage('ETHUSD', 1))
    # asyncio.run(access.set_leverage('XRPUSD', 1))
    # print(asyncio.run(access.access_leverage()))