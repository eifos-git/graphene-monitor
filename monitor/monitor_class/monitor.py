from monitor_class.AbstractMonitor import AbstractMonitor


class Monitor(AbstractMonitor):

    def __init__(self, config):
        super().__init__(config)

    def set_source(self):
        super().set_source()
        pass

    def add_trigger(self):
        super().add_trigger()
        pass

    def add_actions(self):
        super().set_actions()
        pass





