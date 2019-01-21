from trigger.AbstractTrigger import AbstractTrigger
IMPLEMENTED_COMPARATORS = ["!=", "unequal", "ue",
                           "==", "equal", "eq",
                           ">", "greater", ]


class ValueCompare(AbstractTrigger):

    trigger_conditions = []

    def __init__(self, config):
        super().set_config(config)

    def prepare_message(self):
        data = self.get_config("source_value")
        message = ""
        message += "Trigger: {0} fired!\n".format(self.get_config("name"))
        message += "Data returned is {0}\n".format(data)
        message += "Trigger conditions:\n"
        for (key, value) in self.config.items():
            cfunc = evaluate_trigger_condition(key, value, data)
            if cfunc is True:
                message += "   - Data {0} {1}\n".format(key, value)
            elif cfunc is None:
                pass  # Config data not used for the message
            else:
                raise ValueError("This should not happen")
        return message

    def check_condition(self, data):
        super().check_condition(data) # add data to config as source_value

        if type(data) not in [int, float, bool]:
            raise TypeError("Value_Compare can only compare int, float or bool")

        for (key, value) in self.config.items():
            cfunc = evaluate_trigger_condition(key, value, data)
            if cfunc is not None:
                if not cfunc:
                    # One trigger condition is false and therfore it shouldnt fire
                    # We return it anyway to enable groupings
                    self.fire_condition_met = False
                    return self.config
            cfunc = None
        self.fire_condition_met = True
        return self.config


def evaluate_trigger_condition(key, value, data):
    """Evaluates whether the defined condition is met.
    If not return None ot indicate that the key was not meant for trigger evaluation(i.e. level)
    """
    if key in ["!=", "unequal", "ue"]:
        return value != data

    if key in ["==", "equal", "eq"]:
        return value == data

    if key in [">", "greater", "gr"]:
        return data > value

    if key in [">=", "greater_or_equal", "ge"]:
        return data >= value

    if key in ["<", "less", "ls"]:
        return data < value

    if key in ["<=", "less_or_equal", "le"]:
        return data <= value

    return None
