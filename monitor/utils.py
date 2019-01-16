"""Maps all the config values to their classes"""
from source import *
from trigger import *
from action import *

MAP_SOURCE_TO_CLASS = {"http": http.Http}
MAP_TRIGGER_TO_CLASS = {"value_compare": value_compare.Value_Compare}
MAP_ACTION_TO_CLASS = {"log": log.Log, "console": console.Console}


def get_class_for_source(source):
    return MAP_SOURCE_TO_CLASS[source]


def get_class_for_trigger(trigger):
    return MAP_TRIGGER_TO_CLASS[trigger]


def get_class_for_action(action):
    return MAP_ACTION_TO_CLASS[action]

