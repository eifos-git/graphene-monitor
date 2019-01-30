from abc import ABC, abstractmethod
from monitor.trigger.utils import collapse_triggers
from trigger.AbstractTrigger import AbstractTrigger
from monitor_variations.factory import Factory
import logging


class AbstractMonitor(ABC):
    """Abstract monitor class that is used to set up the monitor as defined in config"""

    def __init__(self, config, name=None):
        self.name = name
        self.source = None
        self.triggers = list()
        self.actions = list()
        self.source_config = config["source"]
        self.triggers_config = config["triggers"]
        self.actions_config = config["actions"]

    def do_monitoring(self):
        """Called once every monitor cycle to calculate whether the triggers have to fire or not"""
        data = self.source.retrieve_data()
        if data is None:  # Problem with source
            return self.handle_no_data()

        triggers = []
        for trigger in self.triggers:
            if trigger.check_condition(data):
                triggers.append(trigger)
        triggers = collapse_triggers(triggers)

        for trigger in triggers:
            if trigger.get_condition() is False:
                continue
            message = "The following Monitor fired: {0}\n".format(self.name) + str(trigger.prepare_message())
            try:
                trigger_level = trigger.get_level()
            except KeyError:
                logging.error("No level provided for trigger, therefore it never fires!")
                continue
            for action in self.actions:
                if trigger_level >= action.get_level():
                    action.fire(message)

    @abstractmethod
    def set_source(self, source):
        """
        :param source: One of the source defined in
        :type source: str
        """
        source = Factory.get_class_for_source(source)
        if self.source is not None:
            print("only one source can be added. Will be ignored!")
        else:
            self.source = source(self.source_config)

    @abstractmethod
    def add_triggers(self, triggers):
        """Add a list of triggers to the monitro that will be tested every monitor iteration.

        :param triggers: List of triggers defined in the config file.
        """
        if type(triggers) is not list:
            triggers = [triggers]
        for trigger in triggers:
            if len(trigger) != 1:
                raise AttributeError("This program doesn't support Triggers nested inside of triggers. "  
                                     "Please remove any list inside of the trigger")
            for trigger_name, trigger_cfg in trigger.items():
                trigger_type = self.get_trigger_type(trigger_name)
            trigger_type = Factory.get_class_for_trigger(trigger_type)
            if trigger_type is None:
                continue
            trigger_cfg["name"] = trigger_name  # Save the name of the trigger to enable a more meaningful action
            trigger = trigger_type(trigger_cfg)
            assert(issubclass(type(trigger), AbstractTrigger))
            self.triggers.append(trigger)

    @abstractmethod
    def add_actions(self, actions):
        """Add all the actions defined in the config file as a list to the monitor class and initializes
        those action classes
        """

        if type(actions) is not list:
            actions = [actions]
        for action in actions:
            if len(action) != 1:
                raise AttributeError("This program doesn't support multiple actions within one action. "
                                     "Please remove any list from the action")

            for action_name, action_cfg in action.items():
                action_type = self.get_action_type(action_name)
            action_type = Factory.get_class_for_action(action_type)
            if action_type is None:
                continue
            action = action_type(action_cfg)
            self.actions.append(action)

    @abstractmethod
    def handle_no_data(self, level=None):
        """Handles the trigger source not available.
        :param level: None means that all actions will fire, otherwise it uses the usual level convention"""

        for action in self.actions:
            if level is None or action.get_level() <= level:
                action.fire("The following monitor fired: {0}\n"
                            "Trigger: UnreachableSourceTrigger\n"
                            "The source {1} is unreachable.\n".format(self.name, self.source.config))

    def _get_config(self, monitor_domain, value, subclasses=None):
        """TODO: This is lazy coding to make it work at the time. There might be some cases in\
        which this function fails.

        Usage: Get the setting for <value> from the current Monitor. Everytime yaml uses a list,
            subclasses decides where to go next

        param monitor_domain: either source/triggers/action or s/t/a
        param value: value to be searched for. If the value is defined multiple times for one monitor,
            i.e. level use the parameter subclasses
        param subclasse: Has to be a list! In case of ambiguity enter the name of the subclass.
            i.e. subclasses=["trigger1"] if you want the config of trigger 1"""

        if monitor_domain in ["s", "source"]:
            config = self.source_config
        elif monitor_domain in ["t", "triggers"]:
            config = self.triggers_config
        elif monitor_domain in ["a", "actions"]:
            config = self.actions_config
        else:
            raise ValueError("monitor_domain hast to be either 'source', 'triggers' or 'actions'")

        def search_recursively(config, value, subclasses):
            if type(config) is list:
                if type(subclasses) is not list:
                    raise TypeError("Subclasses has to be a list")
                subclass = subclasses.pop(0)
                for entries in config:
                    if subclass in entries:
                        return search_recursively(entries[subclass], value, subclasses)

            for key in config:
                if key == value:
                    return config[key]
                if type(config[key]) is list:
                    srlist = search_recursively(config[key], value, subclasses)
                    if list is not None:
                        return srlist
            return None

        sr = search_recursively(config=config, value=value, subclasses=subclasses)

        return sr

    def get_trigger_type(self, trigger_name):
        return self._get_config("triggers", "type", [trigger_name])

    def get_action_type(self, action_name):
        return self._get_config("actions", "type", [action_name])

    def get_error_level(self):
        return self._get_config("source", "error_level")
