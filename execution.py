from TradingSystem.TradingSystem import TradingSystem
from utils.market_utils import *
def execution(STOP_EVENT):
    wait_status = wait_until_920()
    if not wait_status: 
        print("Time over")
        return
    trading_system = TradingSystem.get_instance()
    trading_system.initialize_trading_system()
    trading_system.run_trading_system(STOP_EVENT)
    
