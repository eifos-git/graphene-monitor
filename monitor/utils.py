"""Maps all the config values to their classes"""
from source import *
from trigger import *
from action import *

MAP_SOURCE_TO_CLASS = {"http": http.Http}
MAP_TRIGGER_TO_CLASS = {"value_compare": valuecompare.ValueCompare}
MAP_ACTION_TO_CLASS = {"log": log.Log, "console": console.Console}


def get_class_for_source(source):
    try:
        return MAP_SOURCE_TO_CLASS[source]
    except KeyError:
        raise KeyError("The source specified in config cannot be found. Check for "
                       "typos and make sure to add the source to monitor/utils.py")


def get_class_for_trigger(trigger):
    try:
        return MAP_TRIGGER_TO_CLASS[trigger]
    except KeyError:
        raise KeyError("The trigger specified in config cannot be found. Check for "
                       "typos and make sure to add the trigger to monitor/utils.py")


def get_class_for_action(action):
    try:
        return MAP_ACTION_TO_CLASS[action]
    except KeyError:
        raise KeyError("The actino specified in config cannot be found. Check for "
                       "typos and make sure to add the action to monitor/utils.py")
