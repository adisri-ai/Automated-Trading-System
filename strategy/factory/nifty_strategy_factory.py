from strategy.factory.strategy_factory import StrategyFactory
from strategy.Nifty_Calendar_Strategy import NiftyCalendarStrategy
class NiftyStrategyFactory(StrategyFactory):
    def create_strategy(**kwargs):
        broker = kwargs.get("broker" , None)
        expiry_manager = kwargs.get("expiry_manager" , None)
        repository = kwargs.get("repository" , None)
        option_selector = kwargs.get("option_selector"  , None)
        pnl_engine = kwargs.get("pnl_engine" , None)
        return NiftyCalendarStrategy(broker , expiry_manager , repository , option_selector , pnl_engine)
