from abc import ABC, abstractmethod

class AbstractTrigger(ABC):
    config = None
    def set_config(self, config):
        self.config = config

    @abstractmethod
    def check_condition(self):
        """Decides, whether the trigger condition is met and therefore if it shoots"""

    def get_config(self, value):
        return self.config[value]
