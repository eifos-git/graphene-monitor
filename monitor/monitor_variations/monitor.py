from monitor_variations.AbstractMonitor import AbstractMonitor


class Monitor(AbstractMonitor):

    def __init__(self, config):
        super().__init__(config)
        self.set_source(self.get_config("source", "type"))
        self.add_triggers(self.get_config("triggers", "list"))
        self.add_actions(self.get_config("action", "list"))
        print("Monitor building finished successfully")

    def set_source(self, source):
        super().set_source(source=source)

    def add_triggers(self, triggers):
        super().add_triggers(triggers=triggers)

    def add_actions(self, actions):
        super().add_actions(actions=actions)





