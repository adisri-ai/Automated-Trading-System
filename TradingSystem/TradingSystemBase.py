from abc import ABC , abstractmethod
class TradingSystemBase(ABC) : 
    @abstractmethod
    def initialize_trading_system(self):
        pass
    @abstractmethod
    def run_trading_system(self):
        pass
    @abstractmethod 
    def shutdown_trading_system(self):
        pass
