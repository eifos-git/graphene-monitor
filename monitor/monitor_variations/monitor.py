from monitor_variations.AbstractMonitor import AbstractMonitor


class Monitor(AbstractMonitor):

    def __init__(self, config):
        super().__init__(config)
        self.set_source(self.get_config("source", "type")) #
        self.add_trigger(self.get_config("triggers", "list"))
        self.add_action()
        print("Monitor building finished successfully")

    def set_source(self, source):
        super().set_source(source=source)
        pass

    def add_trigger(self, trigger):
        super().add_trigger(trigger=trigger)
        pass

    def add_action(self):
        super().add_action()
        pass





