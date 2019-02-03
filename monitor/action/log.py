from . import AbstractAction
import logging
import time


class Log(AbstractAction):

    def __init__(self, config):
        super().__init__(config)

    def fire(self, message):
        print("fire")
