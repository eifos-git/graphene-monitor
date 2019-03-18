from . import AbstractTrigger
import logging


class ValueCompare(AbstractTrigger):
    """Compare Value returned from source with another value.
    Data has to be of type int, float or bool as the operator are not defined for other datatypes.
    Config values are:

    * <operator>: <operand> (look at :func:`evaluate_trigger_condition` for more details
    * <operator2>: <operand> multiple operators, logical AND
    """

    def prepare_message(self):
        data = self.get_data()
        message = ""
        message += "Trigger: {0}\n".format(self.get_config("name"))
        message += "Data: {0}\n".format(data)
        message += "Conditions:\n"
        for (key, value) in self.config.items():
            cfunc = evaluate_trigger_condition(key, data, value)
            if cfunc is True:
                message += "   - Data {0} {1}".format(key, value)
            elif cfunc is None:
                pass  # Config data not used for the message
        return message

    def check_condition(self, data):
        """Checks whether or not data meets the requirements specified in config for this trigger"""
        if type(data) not in [int, float, bool]:
            logging.error("Value_Compare can only compare int, float or bool")
            return False

        for (key, value) in self.config.items():
            cfunc = evaluate_trigger_condition(key, data, value)
            if cfunc is not None:
                if not cfunc:
                    # One trigger condition is false and therefore it shouldn't fire
                    # We return it anyway to enable groupings
                    return False
            cfunc = None
        return True


def evaluate_trigger_condition(key, data, value):
    """Evalute the condition of this trigger. Available operator are:

    * unequal (ue)
    * equal (eq)
    * greater (gr)
    * greater_or_equal (ge)
    * less (ls)
    * less_or_equal (le)

    as well as their corresponding python operators an a short version (in brackets).

    :param key: Or operand that is used for the calculation.
    :param data: Data returned from source
    :param value: Value data gets compared with.
    :return: bool(data key value), e.g. bool(1 == 0) for data=1, key=equal, value=0
    """
    if key in ["!=", "unequal", "ue"]:
        return data != value

    if key in ["==", "equal", "eq"]:
        return data == value

    if key in [">", "greater", "gr"]:
        return data > value

    if key in [">=", "greater_or_equal", "ge"]:
        return data >= value

    if key in ["<", "less", "ls"]:
        return data < value

    if key in ["<=", "less_or_equal", "le"]:
        return data <= value

    return None
