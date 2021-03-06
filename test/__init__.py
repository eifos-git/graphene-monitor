from monitor.source import AbstractSource
from monitor.trigger import AbstractTrigger
from monitor.action import AbstractAction


class MockSource(AbstractSource):
    def retrieve_data(self):
        self._set_data(0)


class MockBuffer(AbstractSource):
    def __init__(self, source_config, source_name):
        self._index = 0
        self._buffer = [0, 0, 1, 420]
        super().__init__(source_config, source_name)

    def retrieve_data(self):
        data = self._buffer[self._index % len(self._buffer)]
        self._index += 1
        if data == 420:
            self._set_data()
            return
        self._set_data(data)


class MockTrigger(AbstractTrigger):
    def check_condition(self, data):
        super().check_condition(data)
        if data != 0:
            self.fire_condition_met = False
            return False
        self.fire_condition_met = True
        return True

    def prepare_message(self):
        return "Mock Trigger ok"


class MockAction(AbstractAction):
    def __init__(self, config):
        super().__init__(config)

    def fire(self, message):
        f = open("test_do_monitoring.txt", "w")
        f.write(message)
        f.close()

