from abc import ABC, abstractmethod
from utils import get_classname_for_config
import logging
import copy


class AbstractMonitor(ABC):
    """Abstract Monitor is the outermost framework for the monitor program.
    It is implemented as an Abstract class but mostly used as a normal class.
    Monitor inherits from Abstract Monitor but add almost no functionality, because all
    of the methods in Abstract Monitor are mandatory.

    Init and the three "add"-functions are called before the first data is evaluated to
    set the program up.
    Every monitor iteration the function do_monitoring is executed."""

    def __init__(self, config, name=None):
        self.name = name
        self.sources = list()
        self.triggers = list()
        self.actions = list()
        self.sources_config = config["sources"]
        self.triggers_config = config["triggers"]
        self.actions_config = config["actions"]

    def _get_config(self, monitor_domain, value=None, subclasses=None):
        """TODO: This is lazy coding to make it work at the time. There might be some cases in\
        which this function fails.

        Usage: Get the setting for <value> from the current Monitor. Everytime yaml uses a list,
            subclasses decides where to go next

        param monitor_domain: either source/triggers/action or s/t/a
        param value: value to be searched for. If the value is defined multiple times for one monitor,
            i.e. level use the parameter subclasses
            Value can be non to indicate that you want the config for a whole domain
        param subclasse: Has to be a list! In case of ambiguity enter the name of the subclass.
            i.e. subclasses=["trigger1"] if you want the config of trigger 1"""

        if monitor_domain in ["s", "sources"]:
            config = self.sources_config
        elif monitor_domain in ["t", "triggers"]:
            config = self.triggers_config
        elif monitor_domain in ["a", "actions"]:
            config = self.actions_config
        else:
            raise ValueError("monitor_domain hast to be either 'sources', 'triggers' or 'actions'")

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

        if value is None:
            return config

        sr = search_recursively(config=config, value=value, subclasses=subclasses)

        return sr

    def add_sources(self, sources):
        """Add sources to the monitor

        :param sources: List of dictionaries with exactly one key to value pair each.
            The key is used as the name of the source and the value is used as
            the configuration of the source.
            Note that the name doesnt actually matter. It is mostly used for more meaningful debugging
            messages and occasionally to retrieve the correct config value (see _get_config())
        """
        if not isinstance(sources, list):
            sources = [sources]
        for source in sources:
            if len(source) != 1:
                raise AttributeError("Config File wrong. This application does not support lists of sources"
                                     "nested inside of sources.")

            try:
                for source_name, source_cfg in source.items():  # Only iterates once if the config is setup correctly
                    source_type = self.get_source_type(source_name)
                src_module, src_class = get_classname_for_config(source_type)
                module = __import__(src_module, fromlist=[src_class])
                klass = getattr(module, src_class)
                source = klass(source_cfg, source_name=source_name)
                self.sources.append(source)
            except ModuleNotFoundError:
                logging.error("Unable to find the Module you specified for {0}".format(source_name))
                continue
            except AttributeError:
                logging.error("Missing or wrong source.class Attribute in {0}".format(source_name))
                continue
            except TypeError:
                logging.error("Missing source.class Attribute in {0}".format(source_name))
                continue

    def add_triggers(self, triggers):
        """Add triggers to the monitor

        :param triggers: List of dictionaries with exactly one key to value pair each.
            The key is used as the name of the trigger and the value is used as
            the configuration of the trigger.
            Note that the name doesnt actually matter. It is mostly used for more meaningful debugging
            messages occasionally to retrieve the correct config value (see _get_config())
        """
        if not isinstance(triggers, list):
            triggers = [triggers]
        for trigger in triggers:
            if len(trigger) != 1:
                raise AttributeError("This program doesn't support Triggers nested inside of triggers. "  
                                     "Please remove any list inside of the trigger")
            try:
                for trigger_name, trigger_cfg in trigger.items():  # Only iterates once if the config is setup correctly
                    trigger_type = self.get_trigger_type(trigger_name)  # path to the class of our trigger
                trg_module, trg_class = get_classname_for_config(trigger_type)
                module = __import__(trg_module, fromlist=[trg_class])
                klass = getattr(module, trg_class)
                trigger_cfg["name"] = trigger_name  # Save the name of the trigger to enable a more meaningful action
                trigger = klass(trigger_cfg)
                self.triggers.append(trigger)
            except ModuleNotFoundError:
                logging.error("Unable to find the Module you specified for trigger " + trigger_name)
                continue
            except AttributeError:
                logging.error("Missing or wrong trigger.class Attribute in " + trigger_name)
                continue
            except TypeError:
                logging.error("Missing trigger.class Attribute in " + trigger_name)

    def add_actions(self, actions):
        """Add actinosto the monitor

        :param actions: List of dictionaries with exactly one key to value pair each.
            The key is used as the name of the action and the value is used as
            the configuration of the action.
            Note that the name doesnt actually matter. It is mostly used for more meaningful debugging
            messages and occasionally to retrieve the correct config value (see _get_config())
        """
        if not isinstance(actions, list):
            actions = [actions]
        for action in actions:
            if len(action) != 1:
                raise AttributeError("This program doesn't support Triggers nested inside of triggers. "  
                                     "Please remove any list inside of the trigger")
            try:
                for action_name, action_cfg in action.items():  # Only iterates once if the config is setup correctly
                    action_type = self.get_action_type(action_name)  # path to the class of our trigger
                action_module, action_class = get_classname_for_config(action_type)
                module = __import__(action_module, fromlist=[action_class])
                klass = getattr(module, action_class)
                action_cfg["name"] = action_name  # Save the name of the trigger to enable a more meaningful action
                action = klass(action_cfg)
                self.actions.append(action)
            except ModuleNotFoundError:
                logging.error("Unable to find the Module you specified for {0}".format(action_name))
                continue
            except AttributeError or TypeError:
                logging.error("Missing or wrong action.class Attribute in {0}".format(action_name))
                continue

    def do_monitoring(self):
        """Called once every monitor cycle to calculate whether the triggers have to fire or not"""
        data = []
        for source in self.sources:
            new_data = source.retrieve_data()
            if new_data is not None:
                data.append(new_data)
            else:
                # TODO is it useful to make this part of source
                self.handle_no_data(source)

        triggers = []
        for trigger in self.triggers:
            for dataX in data:
                # Trigger needs to be evaluated for every data separately
                trigg = copy.deepcopy(trigger)
                if trigg.check_condition(dataX):
                    if trigg.fired_recently() is True:
                        #  The trigger condition is True but it fired too recently. Therefore we skip it
                        trigger.deactivate_trigger()
                    else:
                        trigger.update_last_time_fired()
                        triggers.append(trigg)
        #  triggers = collapse_triggers(trigger) Group Support - Not used anymore

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

    def handle_no_data(self, source, level=None):
        """Handler that prepares a message for each source that is not available.

        :param source: Object of type AbstractSource that
        :param level: None means that all actions will fire, otherwise it uses the usual level convention"""

        for action in self.actions:
            if level is None or action.get_level() <= level:
                action.fire("The following monitor fired: {0}\n"
                            "Trigger: Handle no data trigger\n"
                            "The source {1} is unreachable.\n".format(self.name, source.get_source_name()))

    def get_source_type(self, source_name):
        return self._get_config("sources", "class", [source_name])

    def get_trigger_type(self, trigger_name):
        return self._get_config("triggers", "class", [trigger_name])

    def get_action_type(self, action_name):
        return self._get_config("actions", "class", [action_name])

    def get_error_level(self):
        return self._get_config("sources", "error_level")


class Monitor(AbstractMonitor):

    def __init__(self, config, name=None):
        super().__init__(config, name)
        self.add_sources(self._get_config("sources"))
        self.add_triggers(self._get_config("triggers"))
        self.add_actions(self._get_config("actions"))
