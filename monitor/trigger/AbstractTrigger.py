from abc import ABC, abstractmethod

class AbstractTrigger(ABC):
    config = None
    def set_config(self, config):
        self.config = config

    def get_config(self, value):
        return self.config[value]

    @abstractmethod
    def check_condition(self, data):
        """Decides, whether the trigger condition is met and therefore if it shoots"""
        print("Checking Condition")