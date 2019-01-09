from abc import ABC, abstractmethod

class AbstractTrigger(ABC):

    @abstractmethod
    def set_trigger(self):
        pass
