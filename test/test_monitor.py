import unittest
from unittest import mock
from monitor.monitor import AbstractMonitor, SourceTriggerPair, Monitor
from monitor import Config, start_working, setup_monitors
import logging
import


class TestAbstractMonitor(unittest.TestCase):
    def setUp(self):
        Config.add_general_config(dict(config="test_monitor.yaml"))
        log = logging.getLogger(__name__)
        Config.load_monitor_config()

        self.monitors = setup_monitors()


if __name__ == "__main__":
    unittest.main()