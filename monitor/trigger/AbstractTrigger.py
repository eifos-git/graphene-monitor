from abc import ABC, abstractmethod

class AbstractTrigger(ABC):
    config = None
    fire_condition_met = False

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

    def get_condition(self):
        return self.fire_condition_met

    def deactivate_trigger(self):
        """The trigger can be disabled after its evaluation to enable group support.
        See trigger/utils/collapse_triggers"""
        self.fire_condition_met = False

    @abstractmethod
    def check_condition(self, data):
        """Decides, whether the trigger condition is met and therefore if it shoots,
        """
        self.config["source_value"] = data


    @abstractmethod
    def prepare_message(self):
        """Message to be sent to action. A more meaningful method should be implemented
        for a specifig trigger"""

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
