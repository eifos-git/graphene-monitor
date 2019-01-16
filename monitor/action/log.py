from action.AbstractAction import AbstractAction


class Log(AbstractAction):

    def __init__(self, config):
        super().set_config(config)

    def fire(self):
        print("Printing message to log file")
