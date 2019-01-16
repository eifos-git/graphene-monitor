from action.AbstractAction import AbstractAction

class Console(AbstractAction):
    """Console is a type of action that only prints messages to the console"""

    def __init__(self, config):
        super().set_config(config)

    def shoot(self):
        print("Printing message to console")

