from . import AbstractAction

class Console(AbstractAction):
    """Console is a type of action that only prints messages to the console"""

    def __init__(self, config):
        super().__init__(config)

    def fire(self, message):
        print(message)

