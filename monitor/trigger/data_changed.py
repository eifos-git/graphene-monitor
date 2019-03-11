from . import AbstractTrigger


class DataChanged(AbstractTrigger):
    """Trigger that fires whenever data changes or doesn't change.
    Current data is saved in ram."""

    def __init__(self, config):
        super().__init__(config)
        self.trigger_conditions = False
        self.old_data = None

    def prepare_message(self):
        return "Data has changed! From {0} to {1}\n".format(self.old_data.old_data, self.old_data.data)

    def get_reverse(self):
        """Get the reverse config. Default is set to False"""
        return self.get_config("reverse", ignore=True, default=False)

    def check_condition(self, data):
        if self.old_data is None:
            # first monitor iteration doesnt fire by convention
            self.old_data = OldData(data)
            return False
        else:
            reverse = self.get_reverse()
            if reverse:
                return self.old_data.has_not_changed(data)
            return self.old_data.has_changed(data)


class OldData:
    """A class to save the old data that is supposed to be evaluated in the next monitor cycle"""
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

    def has_not_changed(self, new_data):
        if self.hash != hash(new_data):
            self.old_data = self.data
            self.data = new_data
            self.hash = hash(new_data)
            return False
        else:
            return True


