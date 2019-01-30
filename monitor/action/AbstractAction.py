from abc import ABC, abstractmethod


class AbstractAction(ABC):

    def __init__(self, action_config):
        self.config = action_config
        # level_redundancy: If True all actions with a level smaller than the triggerlevel will be executed as well
        self.set_config()

    def set_config(self):
        """See AbstractSource"""
        self.level = self.get_config("level")
        try:
            self.level_redundancy = self.get_config("level-redundancy")
            print("lr set to True")
        except KeyError:
            pass

    def get_config(self, config_title):
        """See AbstractSource"""
        return self.config[config_title]

    def get_level(self):
        return self.level

    @abstractmethod
    def fire(self, message):
        """This method is called, whenever some trigger conditions are met"""


