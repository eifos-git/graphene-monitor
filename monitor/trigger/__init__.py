from abc import ABC, abstractmethod
import time
import logging


class AbstractTrigger(ABC):

    def __init__(self, config):
        self.config = config
        self.fire_condition_met = False
        self._last_time_fired = None
        self.downtime = self._set_downtime()

    def _set_downtime(self):
        downtime = self.get_config("downtime", ignore=True)
        if downtime is None:
            from monitor import Config
            downtime = Config.get_trigger_downtime()
        return downtime

    def get_config(self, value, ignore=False, default=None):
        """
        :param value: Config you are looking for
        :param ignore: if True it ignores KeyErrors (i.e. missing configs) and
            silently returns None
        :param default: Can be returned as defualt value, but only if ignore is set
        """
        try:
            self.config[value]
            return self.config[value]
        except KeyError:
            if ignore:
                return default
            else:
                logging.warning("Missing config value {0} in trigger".format(value))
                return None

    def get_downtime(self):
        return self.downtime

    def get_condition(self):
        return self.fire_condition_met

    def check_source(self, current_source_name):
        """Test for a source name whether this trigger is supposed to handle and evaluate
        the data retrieved from it.
        No source in the config for trigger is treated as if every source is accepted

        :param current_source_name: The name of the source to be tested
        :return bool: Whether or not this trigger should handle the source's data
        """
        source_name = self.get_config("source", True)
        if source_name is None or source_name == current_source_name:
            return True
        return False

    def get_last_time_fired(self):
        return self._last_time_fired

    def update_last_time_fired(self):
        self._last_time_fired = time.time()

    def update_data(self, new_data):
        self.config["source_value"] = new_data

    def fired_recently(self):
        """Checks the last time the trigger fired and if it happened too recently the trigger
        condition is simply set to False. Otherwise function does nothing.
        """
        if not self.get_condition():
            return False
        last_fire = self.get_last_time_fired()
        if last_fire is None:
            self.update_last_time_fired()
            return False
        if (time.time() - last_fire) <= self.get_downtime():
            self.deactivate_trigger()
            return True
        else:
            self.update_last_time_fired()
            return False

    def deactivate_trigger(self):
        """The trigger can be disabled after its evaluation to enable group support.
        Group Support is disabled and might be removed in the future.
        """
        self.fire_condition_met = False

    def get_level(self):
        return self.get_config("level")

    def get_data(self):
        return self.get_config("source_value")

    def evaluate_trigger_condition(self, data):
        """Wrapper method for check condition. We want to write the new data in the config add it
        to a more meaningful message and additionally we have to set the fire_condition_met attribute to the result
        """
        self.config["source_value"] = data
        condition_met = self.check_condition(data)
        self.fire_condition_met = condition_met
        return condition_met

    @abstractmethod
    def check_condition(self, data):
        """Decides, whether the trigger condition is met and therefore if it shoots,
        """

    def prepare_message(self):
        """Message to be sent to action. A more meaningful method should be implemented
        for a specific trigger"""

        message = ""

        config_for_message = dict(self.config)
        name = self.get_config("name", ignore=True)
        if name:
            config_for_message.pop("name")
            message += "Trigger: " + str(name) + "\n"

        type = self.get_config("type", ignore=True)
        if type:
            message += "Type: " + str(type) + "\n"
            config_for_message.pop("type")

        for (key, value) in config_for_message.items():
            message += str(key) + " = " + str(value) + "\n"

        return message
