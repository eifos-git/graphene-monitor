from trigger.AbstractTrigger import AbstractTrigger
class Value_Compare(AbstractTrigger):
    trigger_conditions = []
    def __init__(self, config):
        super().set_config(config)
        #TODO Add conditions

    def check_condition(self, data):
        print("Checking trigger condition")
        if type(data) not in [int, float]:
            raise TypeError("Value_Compare can only compare int or float")
        trigger_condition = True
        if not trigger_condition:
            return None
        return True
