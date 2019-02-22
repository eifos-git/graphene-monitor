from abc import ABC, abstractmethod
import logging


class AbstractAction(ABC):

    def __init__(self, action_config):
        self.config = action_config
        self.level = self.get_config("level")

    def get_config(self, config_title, ignore=False):
        """Search for a key in Config and returns the value

        :param config_title: action key in your config file
        :param ignore: If false a warning message will be logged
        :return: value of the key in config
        """
        try:
            value = self.config[config_title]
        except KeyError:
            if ignore:
                return None
            else:
                logging.warning("get config of {0} failed".format(config_title))
                return None
        return value

    def get_level(self):
        return self.level

    @abstractmethod
    def fire(self, message):
        """Abstract method.
        Gets called every time a triggers condition is met.
        """
