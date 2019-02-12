from abc import ABC, abstractmethod
import logging


class AbstractSource(ABC):

    def __init__(self, source_config, source_name):
        self.config = source_config
        self._source_name = source_name
        self._data = None
        self._currently_reachable = True

    def _get_config_value(self, key, ignore_key_error=False):
        """Method to retrieve the value of the sources config with a given key.
        If ignore key error is set to True any type of key error is ignored and therefore
        this method can be used as a way to check if a config value already exists

        :param key: key of the value in config
        :param ignore_key_error: Decide how to handle a key error
        :return: Either value if key is found or None if it isn't
        """
        try:
            value = self.config[key]
        except KeyError:
            if ignore_key_error:
                return None
            else:
                logging.error("Key Error in AbstractSource._get_config_value for the key {0}".format(key))
                return None
        return value

    def _set_data(self, value=None):
        """Set Data to a new value. This should only be done by the retrieve message method.
        Value to None indicates that something went wrong when retrieving data and later on
        executes AbstractMonitor.handle_no_data()"""
        self._data = value

    def add_config(self, key, value, overwrite=False):
        """Use this method to add a new key or change the config of your source Object.

        :param key: config key, if already in use the value is only overwritten is overwrite is True
        :param value: new value of the key
        :param overwrite: If true it can be used to overwrite existing settings. Otherwise this function
            will do nothing
        """
        value_for_key = self._get_config_value(key, ignore_key_error=True)
        if value_for_key is None:
            # key doesn't exist yet
            self.config[key] = value
            if overwrite is True:
                # Might indicate wrong usage
                logging.log("AbstractSource.add_config(): Overwrite is True, but value doesn't exist yet")
            return
        if overwrite is True:
            self.config[key] = value
            return
        logging.error("Overwrite a value in source.config that already exists is not possible if you don't "
                      "specifically allow in in the method call.")

    def get_source_name(self):
        """Returns the source name. Can be used to create more meaningful and easier to understand
        error messages.

        :return: source name as defined in config
        """
        return self._source_name

    def get_data(self):
        """Returns the current data value of the source. Data is updated every monitor cycle"""
        return self._data

    def set_is_reachable(self, reachable):
        self._currently_reachable = reachable

    def check_if_currently_reachable(self):
        """Check whether the source is already known to be unreachable."""
        return self._currently_reachable

    @abstractmethod
    def retrieve_data(self):
        """Implemented by the subclasses. The Function that gets called every monitor iteration to
        retrieve the new data that is to be checked by trigger
        """
