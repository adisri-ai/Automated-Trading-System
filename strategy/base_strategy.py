from abc import ABC , abstractmethod
class BaseStrategy(ABC):
    def initialize(self):
        pass
    def evaluate_tick(self , tick , market_data):
        pass
    def handle_monthly_rollover(self):
        pass
    def on_order_complete(self):
        pass
    def on_order_placed(self):
        pass
    def restore(self): 
        pass
    def serialize(self):
        pass
