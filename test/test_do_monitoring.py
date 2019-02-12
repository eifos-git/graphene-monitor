import unittest
import logging
import os
from monitor import Config, setup_monitors
from monitor.monitor import Monitor
from test import MockBuffer, MockTrigger, MockAction


class TestMonitorSetup(unittest.TestCase):
    def setUp(self):
        # Load Config to initialize a Monitor. The actual config doesnt matter
        Config.add_general_config(dict(config="test_do_monitoring.yaml"))
        Config.load_monitor_config()
        monitors = setup_monitors()

        file = open("test_do_monitoring.txt", "w")
        file.write("TestMonitoring")
        self.monitor = monitors[0]

        # Overwrite what the monitor does
        self.monitor.sources = [MockBuffer()]

    def test_output(self):
        self.monitor.do_monitoring()

    def tearDown(self):
        os.remove("test_do_monitoring.txt")
        self.monitor = None


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    unittest.main()
