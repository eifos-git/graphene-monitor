from abc import ABC, abstractmethod
from sources import AbstractSource
from trigger import AbstractTrigger
from actions import AbstractAction

class AbstractMonitor(ABC):
    """Abstract monitor class that is used to set up the monitor as defined in config"""
    def __init__(self, config):
        self.source_config = config["source"]
        self.triggers_config = config["triggers"]
        self.actions_config = config["actions"]

    @abstractmethod
    def set_source(self, source):
        assert(issubclass(AbstractSource))
        if self.source != None:
            print("only one source can be added. Will be ignored!")
        else:
            self.source = source

    @abstractmethod
    def add_trigger(self, trigger):
        assert(issubclass(AbstractTrigger, trigger))
        if self.trigger == None:
            trigger = []
        self.trigger.append(trigger)

    @abstractmethod
    def add_actions(self, action):
        assert(issubclass(AbstractTrigger, action))
        if self.actions == None:
            actions = []
        self.actinos.append(action)


    def get_config(self, monitor_domain, value, subclasses=None):
        """TODO: This is lazy coding to make it work at the time. There might be some cases in\
        which this function fails.

        Usage: Get the setting for <value> from the current Monitor. Everytime yaml uses a list,
            subclasses decides where to go next

        param monitor_domain: either source/triggers/actions or s/t/a
        param value: value to be searched for. If the value is defined multiple times for one monitor,
            i.e. level use the parameter subclasses
        param subclasse: Has to be a list! In case of ambiguity enter the name of the subclass.
            i.e. subclasses=["trigger1"] if you want the config of trigger 1"""

        config = []
        if monitor_domain in ["s", "source"]:
            config = self.source_config
        elif monitor_domain in ["t", "triggers"]:
            config = self.triggers_config
        elif monitor_domain in ["a", "actions"]:
            config = self.actions_config
        else:
            raise ValueError("monitor_domain hast to be either source, triggers or actions")

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
                    if list != None:
                        return srlist
            return None

        sr = search_recursively(config=config, value=value, subclasses=subclasses)

        return sr