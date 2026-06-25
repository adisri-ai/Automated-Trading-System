from abc import ABC , abstractmethod
class StrategyFactory(ABC):
    @abstractmethod
    def create_strategy(**kwargs):
        pass
