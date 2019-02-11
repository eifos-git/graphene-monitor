import unittest
from . import MockTrigger, MockSource
from unittest import mock
from monitor.monitor import AbstractMonitor, SourceTriggerPair, Monitor
from monitor import Config, start_working, setup_monitors
import logging


class TestSourceTriggerPair(unittest.TestCase):
    def setUp(self):
        source_cfg = dict()
        trigger_cfg = dict(source="mock_source")
        self.source = MockSource(source_cfg, "mock_source")
        self.trigger = MockTrigger(trigger_cfg)
        self.st_pair = SourceTriggerPair(self.source, self.trigger)

    def test_init(self):
        self.assertIsNotNone(self.st_pair.check_if_wanted())
        self.assertEqual(self.st_pair.source, self.source)
        self.assertNotEqual(self.st_pair.trigger, self.trigger)

    def test_check_condition(self):
        self.st_pair.source.retrieve_data()
        self.assertTrue(self.st_pair.check_condition())

    def tearDown(self):
        self.trigger = None
        self.st_pair = None
        self.source = None


class TestUnwantedSourceTriggerPair(unittest.TestCase):
    def setUp(self):
        source_cfg = dict()
        trigger_cfg = dict(source="real_source")
        source = MockSource(source_cfg, "mock_source")
        self.trigger = MockTrigger(trigger_cfg)
        self.st_pair = SourceTriggerPair(source, self.trigger)

    def test_st_pair(self):
        self.assertFalse(self.st_pair.check_if_wanted())


class TestAbstractMonitor(unittest.TestCase):
    def setUp(self):
        Config.add_general_config(dict(config="test_monitor.yaml"))
        log = logging.getLogger(__name__)
        Config.load_monitor_config()

        self.monitors = setup_monitors()

    def test_attributes(self):
        print(self.monitors)

if __name__ == "__main__":
    unittest.main()
