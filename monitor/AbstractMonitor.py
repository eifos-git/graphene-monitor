from abc import ABC, abstractmethod

class AbstractMonitor(ABC):
    """Abstract Monitor class that is used to set up the Monitor as defined in config"""
    @abstractmethod
    def set_source(self):
        pass

    @abstractmethod
    def set_trigger(self):
        pass

    @abstractmethod
    def set_actions(self):
        pass
