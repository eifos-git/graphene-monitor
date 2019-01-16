from abc import ABC, abstractmethod

class AbstractAction(ABC):

    @abstractmethod
    def send_message(self):
        pass

    @abstractmethod
    def message(self):
        pass


    """
    abstract action:
        get_trigger
        message 
        send message 
    """
