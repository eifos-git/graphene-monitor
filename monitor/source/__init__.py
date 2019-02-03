from abc import ABC, abstractmethod


class AbstractSource(ABC):

    def __init__(self, source_config):
        self.config = source_config

    def set_config(self, config):
        """Called after initialisation of the child class to save the config locally and
        make get_config usable
        """
        self.config = config

    def get_config(self, config_title):
        """Get configuration of this Source

        :param config_title: title of a variable in config i.e. "type"
        :return: value of config_title
        """
        return self.config[config_title]

    @abstractmethod
    def retrieve_data(self):
        """Impemented by the subclasses. The Function that gets called every monitor iteration to
        retrive the new data to be checked by trigger
        """