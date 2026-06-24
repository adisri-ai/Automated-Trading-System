from broker.broker_adapter import BrokerAdapter
from broker.smartapi_utils.order_manager import OrderManager
from broker.smartapi_utils.websocket_manager import WebSocketManager
from broker.smartapi_utils.fund_manager import FundManager
from broker.smartapi_utils.greeks_engine import GreeksEngine
from broker.smartapi_utils.holdings_manager import HoldingsManager
from broker.smartapi_utils.smartapi_authenticator import SmartApiClient
class SmartAPIAdapter(BrokerAdapter) : 
    def __init__(self , order_manager : OrderManager , 
                 websocket_manager : WebSocketManager,
                 fund_manager : FundManager,
                 greek_engine : GreeksEngine,
                 holdings_manager : HoldingsManager,
                 client):
        self.order_manager = order_manager
        self.websocket_manager = websocket_manager
        self.fund_manager = fund_manager
        self.greek_engine = greek_engine
        self.holdings_manager  = holdings_manager
        self.client = client
    def initialize(self):
        return self.websocket_manager.connect()
    def buy(self, *args, **kwargs):
        return self.order_manager.buy(*args , **kwargs)
    def sell(self , *args , **kwargs):
        return self.order_manager.sell(*args , **kwargs)
    def get_ltp(self, *args, **kwargs):
        return self.greek_engine.get_ltp(*args , **kwargs)
    def get_option_chain(self, *args, **kwargs):
        return self.greek_engine.get_option_chain(*args , **kwargs)
    def terminateSession(self):
        return self.client.terminateSession("CLIENT_CODE")