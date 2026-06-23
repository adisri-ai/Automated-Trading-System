from abc import ABC, abstractmethod

class BrokerAdapter(ABC):
    @abstractmethod 
    def login(self): 
      pass
    @abstractmethod
    def place_order(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_ltp(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_option_chain(self, *args, **kwargs):
        pass
    @abstractmethod 
    def terminateSession(self):
      pass
