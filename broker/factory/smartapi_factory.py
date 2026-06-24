from broker_factory import BrokerFactory
from broker.smartapi_adapter import SmartAPIAdapter
from broker.smartapi_utils.order_manager import OrderManager
from broker.smartapi_utils.websocket_manager import WebSocketManager
from broker.smartapi_utils.fund_manager import FundManager
from broker.smartapi_utils.greeks_engine import GreeksEngine
from broker.smartapi_utils.holdings_manager import HoldingsManager
from broker.smartapi_utils.smartapi_authenticator import SmartApiClient
from broker.smartapi_utils.order_engine import SmartApiOrders
class SmartApiFactory(BrokerFactory) : 
    def create_broker(self):
        self.client = SmartApiClient()
        self.smart = self.client.login()
        self.holdings_manager = HoldingsManager(self.smart)
        self.holdings_manager.refresh_holdings()
        self.fund_manager = FundManager(self.smart)
        self.greeks_engine = GreeksEngine(self.smart)
        self.websocket_manager = WebSocketManager(
                auth_token=self.client.session['data']['jwtToken'],
                api_key=self.client.smart.api_key,
                client_code="CLIENT_CODE",
                feed_token=self.smart.getfeedToken(),
                strategy=None
            )
        self.order_engine = SmartApiOrders(self.smart)
        self.order_manager = OrderManager(self.order_engine , None , self.holdings_manager , self.fund_manager , None)
        return SmartAPIAdapter(self.order_manager , self.websocket_manager , self.fund_manager , 
                               self.greeks_engine , self.holdings_manager , self.client)
    
