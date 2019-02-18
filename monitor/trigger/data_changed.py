from . import AbstractTrigger


class DataChanged(AbstractTrigger):

    def __init__(self, config):
        super().__init__(config)
        self.trigger_conditions = False
        self.old_data = None

    def prepare_message(self):
        return "Data has changed! From {0} to {1}\n".format(self.old_data.old_data, self.old_data.data)

    def check_condition(self, data):

        if self.old_data is None:
            # first monitor iteration doesnt fire by convention
            self.old_data = OldData(data)
            return False
        else:
            return self.old_data.has_changed(data)


class OldData:
    data = None
    hash = None

    def __init__(self, data):
        self.data = data
        self.old_data = None
        self.hash = hash(data)

    def has_changed(self, new_data):
        if self.hash != hash(new_data):
            self.old_data = self.data
            self.data = new_data
            self.hash = hash(new_data)
            return True
        else:
            return False

