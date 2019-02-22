from . import AbstractAction


class Stdout(AbstractAction):
    """Console is a type of action that only prints messages to the console"""

    def fire(self, message):
        print(message)

