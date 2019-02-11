import unittest
import logging
from monitor import Config, start_working, setup_monitors


class TestMonitorSetup(unittest.TestCase):
    def setUp(self):
        Config.add_general_config(dict(config="test_config.yaml"))
        log = logging.getLogger(__name__)
        Config.load_monitor_config()

        self.monitors = setup_monitors()

    def test_monitor_amount(self):
        self.assertEqual(len(self.monitors), 1)

    def test_stp_amount(self):
        self.assertEqual(len(self.monitors[0].st_pairs), 5)


if __name__ == '__main__':
    unittest.main()
