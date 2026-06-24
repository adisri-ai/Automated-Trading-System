from TradingSystem.TradingSystemBase import TradingSystemBase
from strategy.base_strategy import BaseStrategy
from broker.broker_adapter import BrokerAdapter
from persistence.txt_repository import TxtRepository
from core.expiry_manager import ExpiryManager
from core.option_selector.option_selector_base import OptionSelector
from core.runtime_manager import RuntimeManager
from core.pnl_engine import PnlCalculator
class TradingSystem(TradingSystemBase):
    __instance = None
    __PRIVATE_TOKEN = "****"
    def __init__(self , private_token , 
                 strategy : BaseStrategy , 
                 broker : BrokerAdapter,
                 txt_repository : TxtRepository,
                 option_selector : OptionSelector,
                 runtime_manager : RuntimeError,
                 pnl_engine : PnlCalculator):
        if(private_token != TradingSystem.__PRIVATE_TOKEN): return 
        self.strategy = strategy
        self.broker = broker 
        self.txt_repository = txt_repository
        self.option_selector = option_selector
        self.pnl_engine = pnl_engine
        self.runtime_manager = runtime_manager
        return 
    @staticmethod
    def check_single_instance(self):
        if(TradingSystem.__instance is not None): return False
        else : return True
    @staticmethod
    def get_instance(self):
        if(TradingSystem.__instance is not None) : return TradingSystem.__instance
    def initialize_trading_system(self):
        self.broker.add_strategy(self.strategy)
    def shutdown_trading_system(self):
        return self.runtime_manager.shutdown()
