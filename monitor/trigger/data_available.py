from . import AbstractTrigger


class DataAvailable(AbstractTrigger):
    """A Trigger that fires every time data is returned from source.
    Note that we have handle no data implemented in monitor.monitor but it only fires when
    source explicitly sets data to None.
    The workaround we recommend for this is setting data to [] if it technically doesn't return any data, as can be
    seen in source.proposal.
    """
    def prepare_message(self):
        data = self.get_data()
        message = "Data Received Trigger\n"
        message += str(data)
        return message

    def check_condition(self, data):
        if data:
            return True
        return False
