from abc import ABC, abstractmethod

class AbstractTrigger(ABC):
    config = None
    def set_config(self, config):
        self.config = config

    def get_config(self, value, ignore=False):
        """
        :param value: Config you are looking for
        :param ignore: if True it ignores KeyErrors (i.e. missing configs) and
            silently returns None
        """
        if ignore:
            try:
                self.config[value]
            except KeyError:
                return None
        return self.config[value]

    @abstractmethod
    def check_condition(self, data):
        """Decides, whether the trigger condition is met and therefore if it shoots"""
