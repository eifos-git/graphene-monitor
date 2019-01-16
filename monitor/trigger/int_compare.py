from trigger.AbstractTrigger import AbstractTrigger
class Int_Compare(AbstractTrigger):
    def __init__(self, config):
        super().set_config(config)

    def check_condition(self):
        return True