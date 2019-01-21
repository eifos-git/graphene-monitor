from action.AbstractAction import AbstractAction
from monitor.action.utils import get_time
import logging
import time


class Log(AbstractAction):

    def __init__(self, config):
        super().set_config(config)

    def fire(self, message):
        logging.basicConfig(filename="monitor.log", filemode="w", format="%(message)s")
        logging.warning(get_time() + " - One trigger of your monitor fired \n" + message)
