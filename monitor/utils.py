"""Maps all the config values to their classes"""
from source import *
from trigger import *

MAP_SOURCE_TO_CLASS = {"http": http.Http}
MAP_TRIGGER_TO_CLASS = {"int_compare": int_compare.Int_Compare}
MAP_ACTION_TO_CLASS = {}


def get_class_for_source(source):
    return MAP_SOURCE_TO_CLASS[source]


def get_class_for_trigger(trigger):
    return MAP_TRIGGER_TO_CLASS[trigger]


def get_class_for_action(action):
    return MAP_ACTION_TO_CLASS[action]

