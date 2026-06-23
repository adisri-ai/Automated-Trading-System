import sys
import time

from broker.smartapi.smartapi_client import SmartApiClient
from broker.smartapi.smartapi_orders import SmartApiOrders
from execution.expiry_manager import ExpiryManager
from execution.order_manager import OrderManager
from execution.fund_manager import FundManager
from execution.holdings_manager import HoldingsManager

from persistence.txt_repository import TxtRepository
import pandas as pd
from market.greeks_engine import GreeksEngine
from market.websocket_manager import WebSocketManager

from strategy.engines.pnl_engine import PnlEngine
from strategy.nifty_calendar_strategy import (
    NiftyCalendarStrategy
)
from strategy.selectors.delta_selector import DeltaSelector

from core.runtime_manager import RuntimeManager
import datetime
import pytz
from utils.market_utils import *

from utils.logger import logger
def run_trading_loop():
    print("Trading loop started....")
    wait_status = wait_until_920()

    if not wait_status:
        print("Time over. Exiting....")
        return

    print("Starting run....")
    client = SmartApiClient()

    smart = client.login()
    print("Login is sucessfull ")
    if not is_market_open(
        smart,
        "NIFTY",
        "99926000"
    ):
        print("Market not open....")
        return
    time.sleep(2)
    repository = TxtRepository()

    holdings_manager = HoldingsManager(smart)

    holdings_manager.refresh_holdings()

    fund_manager = FundManager(smart)
    broker_orders = SmartApiOrders(smart)
    fund_manager.refresh_balance()
    print("Initialzing greeks engine and delta selector...")
    greeks_engine = GreeksEngine(smart)
    pd.DataFrame(greeks_engine.get_option_chain(expiry_type="CURRENT")).to_csv("chain.csv")
    delta_selector = DeltaSelector(smart)
    print("Intiazling pnl Engine...")
    pnl_engine = PnlEngine()
    print("Initializing Expiry and Order manager...")
    expiry_manager = ExpiryManager()
    order_manager = OrderManager(
        broker_orders,
        repository,
        holdings_manager,
        fund_manager
    )
    print("Intializing strategy....")

    strategy = NiftyCalendarStrategy(
        greeks_engine=greeks_engine,

        order_manager=order_manager,

        repository=repository,

        option_selector=delta_selector,

        pnl_engine=pnl_engine,
        fund_manager= fund_manager
    )
    print("Initialzing wbesokcet...")
    order_manager.strategy = strategy
    strategy.order_manager = order_manager
    websocket_manager = WebSocketManager(
        auth_token=client.session['data']['jwtToken'],
        api_key=client.smart.api_key,
        client_code="CLIENT_CODE",
        feed_token=smart.getfeedToken(),
        strategy=strategy
    )
    strategy.websocket_manager = websocket_manager
    print("Calling Initialization.....")
    strategy.initialize()
    runtime_manager = RuntimeManager(
        websocket_manager,
        repository,
        strategy,
        smart
    )

    websocket_manager.connect()

    try:


        while True:
            if datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time() >= datetime.time(15, 18):
                print("Shutting down the system")
                runtime_manager.shutdown()
                print("Trading session over.")
                break
                return

            time.sleep(1)

    except KeyboardInterrupt:
         runtime_manager.shutdown()
         sys.exit()
    except Exception as e:
        print(f"Fatal runtime error: {e}")
        logger.error(f"Fatal runtime error: {e}")

        runtime_manager.shutdown()

def main():
    while True:

        try:
            if datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time() >= datetime.time(15, 18):
                print("Trading session over.")
                sys.exit()
                return
            run_trading_loop()

            logger.info("Trading day complete")
            sys.exit()

        except Exception as e:

            logger.error(f"Restarting system: {e}")

            time.sleep(120)
main()
