from .AbstractMonitor import AbstractMonitor


class Monitor(AbstractMonitor):

    def __init__(self, config, name=None):
        super().__init__(config, name)
        self.add_sources(self._get_config("sources"))
        self.add_triggers(self._get_config("triggers"))
        self.add_actions(self._get_config("actions"))
