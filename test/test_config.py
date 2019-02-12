import unittest
import logging
from monitor import Config, start_working, setup_monitors


class TestMonitorSetup(unittest.TestCase):
    def setUp(self):
        Config.add_general_config(dict(config="test_config.yaml"))
        Config.load_monitor_config()

        self.monitors = setup_monitors()
        pass

    def test_monitor_amount(self):
        self.assertEqual(len(self.monitors), 1)

    def test_config(self):
        self.assertEqual(len(Config.data), 1)
        self.assertEqual(len(Config.data[0]), 1)

    def test_monitor_config(self):
        monitor = self.monitors[0]
        self.assertEqual(len(monitor.config), 3)
        self.assertIsNotNone(monitor._get_config("sources"))
        self.assertIsNotNone(monitor._get_config("triggers"))
        self.assertIsNotNone(monitor._get_config("actions"))

        self.assertEqual(len(monitor.st_pairs), 4)
        self.assertEqual(monitor.st_pairs[0])

    def tearDown(self):
        self.monitors = None
        Config.data = list()


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    unittest.main()
