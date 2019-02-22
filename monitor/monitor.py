from abc import ABC
import logging
from .source_trigger_pair import SourceTriggerPair


def get_classname_for_config(path_to_class):
    """Returns class name and module name for class seperated.
    Example: config.yaml should have an entry in every S/T/A giving the path to
    your implementation e.g.: source_class:monitor.source.http.Http
    To properly import it in python we separate monitor.source.http from Http
    """
    for i in range(len(path_to_class)-1, -1, -1):
        if path_to_class[i] is '.':
            return path_to_class[0:i], path_to_class[i+1:]


class AbstractMonitor(ABC):
    """Abstract Monitor is the outermost framework for this application.
    It is implemented as an Abstract class but mostly used as a normal class.
    Monitor inherits from Abstract Monitor but add almost no functionality, because all
    of the methods in Abstract Monitor are mandatory.

    Init and the three "add"-functions are called before the first data is evaluated to
    set the program up.
    Every monitor iteration the function do_monitoring is executed."""

    def __init__(self, config, name=None, general_config=None):
        self.name = name
        self.config = config
        self.config["general_config"] = general_config

        self.sources = list()  #: List of all the sources of this monitor
        self.triggers = list()  #: List of all the triggers of this monitor
        self.actions = list()  #: List of all the actions of this monitor
        self.st_pairs = list()  #: List of all the combinations of sources and triggers the user wants.

        self._add_sources(config["sources"])
        self._add_triggers(config["triggers"])
        self._add_actions(config["actions"])

        self._combine_sources_and_triggers()

    def _get_config(self, monitor_domain, value=None, subclasses=None):
        """TODO: This is lazy coding to make it work at the time. There may be some cases in\
        which this function fails.

        Usage: Get the setting for <value> from the current Monitor. Every time yaml uses a list,
            subclasses decides where to go next

        param monitor_domain: either source/triggers/action or s/t/a
        param value: value to be searched for. If the value is defined multiple times for one monitor,
            i.e. level use the parameter subclasses
            Value can be non to indicate that you want the config for a whole domain
        param subclasse: Has to be a list! In case of ambiguity enter the name of the subclass.
            i.e. subclasses=["trigger1"] if you want the config of trigger 1"""

        if monitor_domain in ["s", "sources"]:
            config = self.config["sources"]
        elif monitor_domain in ["t", "triggers"]:
            config = self.config["triggers"]
        elif monitor_domain in ["a", "actions"]:
            config = self.config["actions"]
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

    def _get_general_config(self, key):
        """get values for the options in cli.py"""
        try:
            value = self.config["general_config"][key]
        except KeyError:
            return None
        return value

    def _add_sources(self, sources):
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
                logging.error("Missing source.class Attribute in {0}, or wrong instantiation "
                              "of the class".format(source_name))
                continue

    def _add_triggers(self, triggers):
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

    def _add_actions(self, actions):
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

    def _combine_sources_and_triggers(self):
        """Triggers have to explicitly name the sources they want to use.
        In this method we create a pair for every trigger and source that
        want to be combined to a pair together. In the main monitoring method
        those pairs are tested for the triggers conditions

        This is done by adding source in the config of your trigger


        """
        for source in self.sources:
            for trigger in self.triggers:
                st_pair = SourceTriggerPair(source, trigger)
                if st_pair.check_if_wanted():
                    #  This means the pairing is legit and wanted from the user
                    self.st_pairs.append(st_pair)

    def do_monitoring(self):
        """Main method of monitor. Called once every monitor cycle. At first it updates all the sources, secondly
        it goes through all the stpairs and checks their conditions and finally it fires the messages for each
        stpair that is supposed to fire in the according action."""

        for source in self.sources:
            source.retrieve_data()
            if source.get_data() is None:
                # source is unreachable
                self.handle_no_data(source)
            else:
                self.check_if_newly_available(source)

        activated_triggers = []
        for st_pair in self.st_pairs:
            if st_pair.evaluate_trigger_condition():
                activated_triggers.append(st_pair.get_trigger())

        for trigger in activated_triggers:
            message = "The following Monitor fired: {0}\n".format(self.name) + str(trigger.prepare_message())
            try:
                trigger_level = trigger.get_level()
            except KeyError:
                logging.error("No level provided for trigger, therefore it never fires!")
                continue
            for action in self.actions:
                if trigger_level == action.get_level():
                    action.fire(message)
        print("monitor_cycle_finished")

    def handle_no_data(self, source, level=None):
        """Handle no data gets called every time a source doesn't return data for some reason.
        In order to not spam the user about the fact that the source is unreachable, we only
        fire a trigger every time the state of the source changes from available to not available.

        It either fires on every action defined in config """
        if not source.check_if_currently_reachable():
            return

        source.set_is_reachable(False)
        for action in self.actions:
            if level is None or action.get_level() == level:
                action.fire("Monitor: {0}\n"
                            "Trigger: Handle no data trigger\n"
                            "   - {1} is unreachable.\n".format(self.name, source.get_source_name()))

    def check_if_newly_available(self, source):
        """If the source was recently unavailable notifies the user that the source is available again"""
        if not source.check_if_currently_reachable():
            # Marked as unreachable by previous monitor iterations
            source.set_is_reachable(True)
            for action in self.actions:
                action.fire("Source {0} of Monitor {1} is reachable again!\n\n".format(self.name, source.get_source_name()))

    def get_source_type(self, source_name):
        return self._get_config("sources", "class", [source_name])

    def get_trigger_type(self, trigger_name):
        return self._get_config("triggers", "class", [trigger_name])

    def get_action_type(self, action_name):
        return self._get_config("actions", "class", [action_name])

    def get_error_level(self):
        return self._get_config("sources", "error_level")


class Monitor(AbstractMonitor):

    def __init__(self, config, general_config, name=None):
        super().__init__(config, name, general_config)
