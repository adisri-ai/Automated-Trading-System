from TradingSystem.TradingSystemBase import TradingSystemBase
from persistence.txt_repository import TxtRepository
from core.expiry_manager import ExpiryManager
from core.option_selector.nifty_calendar_delta_selector import NiftyCalendarDeltaSelector
from core.runtime_manager import RuntimeManager
from core.pnl_engine import PnlCalculator
from utils.logger import logger
from strategy.factory.nifty_strategy_factory import NiftyStrategyFactory
from broker.factories.smartapi_factory import SmartApiFactory
from datetime import datetime
import pytz
import threading
class TradingSystem(TradingSystemBase):
    __instance = None
    __PRIVATE_TOKEN = "****"
    def __init__(self , private_token):
        if(private_token != TradingSystem.__PRIVATE_TOKEN): return 
        factory = SmartApiFactory()
        self.broker = factory.create_broker()
        self.txt_repository = TxtRepository()
        self.option_selector = NiftyCalendarDeltaSelector(self.broker)
        self.pnl_engine = PnlCalculator()
        self.runtime_manager = RuntimeManager(self.txt_repository , None , self.boker)
        self.expiry_manager = ExpiryManager()
        self.logger = logger
        return 
    @staticmethod
    def check_single_instance():
        if(TradingSystem.__instance is not None): return False
        else : return True
    @staticmethod
    def get_instance():
        if(TradingSystem.__instance is None) : TradingSystem.__instance = TradingSystem(TradingSystem.__PRIVATE_TOKEN)
        return TradingSystem.__instance
    def initialize_trading_system(self):
        factory = NiftyStrategyFactory()
        self.strategy = factory.create_strategy(broker = self.broker , repository = self.txt_repository , 
                                                option_selector= self.option_selector , 
                                                runtime_manager = self.runtime_manager,
                                                expiry_manager = self.expiry_manager,
                                                pnl_engine = self.pnl_engine)
        self.broker.add_strategy(self.strategy)
        self.runtime_manager.strategy = self.strategy
    def run_trading_system(self , STOP_EVENT : threading.Event):
        self.strategy.initialize()
        self.broker.connect()
        try : 
            while not STOP_EVENT.is_set():
                if STOP_EVENT.is_set():

                    print(
                        "Manual stop requested"
                    )

                    self.runtime_manager.shutdown()

                    break
                if datetime.datetime.now(pytz.timezone('Asia/Kolkata')).time() >= datetime.time(15, 18):
                    print("Shutting down the system")
                    self.runtime_manager.shutdown()
                    print("Trading session over.")
                    break
        except KeyboardInterrupt:
            self.runtime_manager.shutdown()
            raise SystemExit
        except Exception as e:
            print(f"Fatal runtime error: {e}")
            self.logger.error(f"Fatal runtime error: {e}")
            self.runtime_manager.shutdown()
    def shutdown_trading_system(self):
        return self.runtime_manager.shutdown()
