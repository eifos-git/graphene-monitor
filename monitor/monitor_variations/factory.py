"""Maps all the config values to their classes"""
from ..source import *
from ..trigger.trigger_type import *
from ..action.action_type import *
import logging


class Factory:
    """Impemented as a Factory (see: DesignPatters - Factory).
    Binds config string to corresponding class
    """

    source_mappings = {"http": http.Http, "pp-balance": peerplays_balance.PeerplaysBalance}

    trigger_mappings = {"value_compare": valuecompare.ValueCompare, "data_changed": data_changed.DataChanged}

    action_mappings = {"log": log.Log,
                       "console": console.Console,
                       "telegram": telegram_action.TelegramAction}

    @staticmethod
    def get_class_for_source(source):
        try:
            return Factory.source_mappings[source]
        except KeyError:
            raise KeyError("The source specified in config cannot be found. Check for "
                           "typos and make sure to add the source to monitor/factory.py")


    @staticmethod
    def get_class_for_trigger(trigger):
        try:
            return Factory.trigger_mappings[trigger]
        except KeyError:
            logging.error("The trigger <{0}> in config cannot be found. Check for typos and "
                          "make sure that the trigger has been added to monitor/factory.py".format(trigger))
            return None


    @staticmethod
    def get_class_for_action(action):
        try:
            return Factory.action_mappings[action]
        except KeyError:
            logging.error("The action <{0}> in config cannot be found. Check for typos and make sure"
                          "that the action has been added to monitor/factory.py".format(action))
            return None
