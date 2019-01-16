from abc import ABC, abstractmethod


class AbstractSource(ABC):
    config = None # Dict of Config as defined in the config file

    def set_config(self, config):
        """Called after initialisation of the child class to save the config locally and
        make get_config usable
        """
        self.config = config

    @abstractmethod
    def retrieve_data(self):
        """Impemented by the subclasses. The Function that gets called every monitor iteration to
        retrive the new data to be checked by trigger
        """
        pass

    def get_config(self, config_title):
        """Get configuration of this Source

        :param config_title: title of a variable in config i.e. "type"
        :return: value of config_title
        """
        return self.config[config_title]
