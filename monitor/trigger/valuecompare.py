from trigger.AbstractTrigger import AbstractTrigger
IMPLEMENTED_COMPARATORS = ["!=", "unequal", "ue",
                           "==", "equal", "eq",
                           ">", "greater", ]


class ValueCompare(AbstractTrigger):

    trigger_conditions = []

    def __init__(self, config):
        super().set_config(config)

    def check_condition(self, data):
        if type(data) not in [int, float]:
            raise TypeError("Value_Compare can only compare int or float")

        for (key, value) in self.config.items():
            cfunc = evaluate_trigger_condition(key, value, data)
            if cfunc is not None:
                if not cfunc:
                    # One trigger condition is false and therfore it shouldnt fire
                    # We return it anyway to enable groupings
                    self.config["fire_condition_met"] = False
                    return self.config
            cfunc = None
        self.config["fire_condition_met"] = True
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
