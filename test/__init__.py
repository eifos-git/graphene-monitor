from monitor.source import AbstractSource
from monitor.trigger import AbstractTrigger


class MockSource(AbstractSource):
    def retrieve_data(self):
        self._set_data(0)


class MockTrigger(AbstractTrigger):
    def check_condition(self, data):
        super().check_condition(data)
        if data != 0:
            return False
        self.fire_condition_met = True
        return True

    def prepare_message(self):
        return "Mock Trigger ok"
