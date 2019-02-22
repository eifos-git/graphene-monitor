from . import AbstractAction
import logging
import time


class Log(AbstractAction):

    def fire(self, message):
        print("fire")
