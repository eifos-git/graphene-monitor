from abc import ABC, abstractmethod

class AbstractAction(ABC):
    config = None
    #: If True all actions with a level smaller than the triggerlevel will be executed as well
    level_redundancy = False

    def set_config(self, config):
        """See AbstractSource"""
        self.config = config
        try:
            self.level_redundancy = self.get_config("level-redundancy")
            print("lr set to True")
        except KeyError:
            pass

    def get_config(self, config_title):
        """See AbstractSource"""
        return self.config[config_title]

    @abstractmethod
    def shoot(self):
        """This method is called, whenever some trigger conditions are met"""
        pass

    """
    abstract action:
        get_trigger
        message 
        send message 
    """
