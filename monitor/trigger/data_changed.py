from . import AbstractTrigger


class DataChanged(AbstractTrigger):

    def __init__(self, config):
        super().__init__()
        self.trigger_conditions = False
        super().set_config(config)
        self.old_data = None

    def prepare_message(self):
        # TODO: Make this more meaningful
        return "Data has changed! New Value is: " + str(self.old_data.data)

    def check_condition(self, data):
        super().check_condition(data)

        if self.old_data is None:
            # first monitor iteration doesnt fire by convention
            self.old_data = OldData(data)
            return self.config
        else:
            self.fire_condition_met = self.old_data.has_changed(data)
        return self.config


class OldData:
    data = None
    hash = None

    def __init__(self, data):
        self.data = data
        self.hash = hash(data)

    def has_changed(self, new_data):
        if self.hash != hash(new_data):
            self.data = new_data
            self.hash = hash(new_data)
            return True
        else:
            return False

