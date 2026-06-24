from datetime import datetime
import pytz
import time
import sys
from strategy.base_strategy import BaseStrategy

from utils.logger import logger
from core.expiry_manager import ExpiryManager
from broker.broker_adapter import BrokerAdapter
from persistence.txt_repository import TxtRepository
from core.option_selector.nifty_calendar_delta_selector import NiftyCalendarDeltaSelector
from core.pnl_engine import PnlCalculator
class NiftyCalendarStrategy(BaseStrategy):

    OPTION_CHAIN_CACHE_SECONDS = 60

    def __init__(
        self,
        broker : BrokerAdapter,
        expiry_manager : ExpiryManager,
        repository : TxtRepository,
        option_selector: NiftyCalendarDeltaSelector,
        pnl_engine : PnlCalculator,
    ):
        self.broker = broker
        self.expiry_manager = expiry_manager


        self.repository = repository

        self.option_selector = option_selector

        self.pnl_engine = pnl_engine
      """
      The remaining code has been hidden to avoid the exposure of the core strategy
      The code does override all the functions in the base_strategy.py file 
      """
