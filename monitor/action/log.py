from . import AbstractAction
import logging
import time


class Log(AbstractAction):
    """Puts output in monitor.log using pythons standard logging library."""

    def fire(self, message):
        logging.warning(message)
