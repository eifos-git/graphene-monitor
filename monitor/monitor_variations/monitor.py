from monitor_variations.AbstractMonitor import AbstractMonitor


class Monitor(AbstractMonitor):

    def __init__(self, config, name=None):
        super().__init__(config, name)
        self.set_source(self._get_config("source", "type"))
        self.add_triggers(self._get_config("triggers", "list"))
        self.add_actions(self._get_config("actions", "list"))

    def set_source(self, source):
        super().set_source(source=source)

    def add_triggers(self, triggers):
        super().add_triggers(triggers=triggers)

    def add_actions(self, actions):
        super().add_actions(actions=actions)

    def do_monitoring(self):
        super().do_monitoring()

    def handle_no_data(self):
        error_level = self.get_error_level()
        if error_level is not None:
            super().handle_no_data(error_level)
        else:
            super().handle_no_data()





