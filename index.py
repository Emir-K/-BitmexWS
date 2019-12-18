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
    parser.add_argument("max_size", type=int, help='Max size')
    parser.add_argument("half_buy_protection", type=float, help="Buy -> Positive, Sell -> Negative")
    parser.add_argument("double_buy_protection", type=float, help="Buy -> Negative, sell ->Positive")
    args = parser.parse_args()
    side = ''
    size = 0
    interval = 0
    tp = 0
    max_size = 0
    half_buy_protection = 0.0
    double_buy_protection = 0.0
    try:
        side = args.side
        size = args.size
        interval = args.interval
        tp = args.tp
        max_size = args.max_size
        half_buy_protection = args.half_buy_protection
        double_buy_protection = args.double_buy_protection
    except Exception as e:
        quit()

    return UserRequest(side,size,interval,tp,max_size,
                       half_buy_protection, double_buy_protection)


if __name__ == "__main__":
    ur = parse_console_input()
    trader = None
    """
    Decide which type of trader (Sell or Buy)
    """
    if ur.get_side() == 'Buy':
        access = ApiAccessBuy()
        trader = TraderBuy(access, ur)
    elif ur.get_side() == 'Sell':
        access = ApiAccessSell()
        trader = TraderSell(access, ur)
    """
    REMOVE ALL TRADES FIRST!
    """
    asyncio.run(trader.remove_all_first())
    """
    Start First Trade!
    """
    asyncio.run(trader.trade())
    """
    wait 30 secs and
    Put it into interval
    """
    time.sleep(ur.time_interval)
    trader.start_trade()






    # asyncio.run(access.set_leverage('BTCUSD', 1))
    # asyncio.run(access.set_leverage('EOSUSD', 1))
    # asyncio.run(access.set_leverage('ETHUSD', 1))
    # asyncio.run(access.set_leverage('XRPUSD', 1))
    # print(asyncio.run(access.access_leverage()))