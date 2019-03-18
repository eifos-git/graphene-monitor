import unittest
from unittest.mock import MagicMock
from . import MockTrigger
from monitor.trigger.valuecompare import ValueCompare, evaluate_trigger_condition
from monitor.trigger.data_changed import DataChanged


class TestValueCompare(unittest.TestCase):
    def setUp(self):
        config = {'class': 'monitor.trigger.valuecompare.ValueCompare', 'greater': 210, 'downtime': 10,
                  'level': 2, 'name': 'TestTrigger'}
        self.trigger = ValueCompare(config)

    def test_evaluate_trigger_condition(self):
        self.assertTrue(evaluate_trigger_condition("==", 10, 10))
        self.assertTrue(evaluate_trigger_condition("!=", 11, 10))
        self.assertTrue(evaluate_trigger_condition(">=", 10, 10))
        self.assertTrue(evaluate_trigger_condition(">", 11, 10))
        self.assertTrue(evaluate_trigger_condition("<=", 10, 10))
        self.assertTrue(evaluate_trigger_condition("<", 9, 10))

        self.assertFalse(evaluate_trigger_condition("==", 11, 10))
        self.assertFalse(evaluate_trigger_condition("!=", 10, 10))
        self.assertFalse(evaluate_trigger_condition(">=", 9, 10))
        self.assertFalse(evaluate_trigger_condition(">", 10, 10))
        self.assertFalse(evaluate_trigger_condition("<=", 11, 10))
        self.assertFalse(evaluate_trigger_condition("<", 10, 10))

    def tearDown(self):
        self.trigger = None
        self.ms = None


class TestAbstractTrigger(unittest.TestCase):
    def setUp(self):
        config = {'class': 'monitor.trigger.valuecompare.ValueCompare', 'greater': 210, 'downtime': 10,
                  'level': 2, 'name': 'TestAbstractTrigger'}
        config_src = config.copy()
        config_src["source"] = "MockSource"
        self.trigger_src = MockTrigger(config_src)
        self.trigger = MockTrigger(config)

    def test_init(self):
        self.assertNotEqual(self.trigger, self.trigger_src)

    def test_get_level(self):
        self.assertEqual(self.trigger.get_level(), 2)

    def test_deactivate_trigger(self):
        self.trigger.check_condition(1)
        self.trigger.deactivate_trigger()
        self.assertFalse(self.trigger.get_condition())

    def test_check_source(self):
        self.assertTrue(self.trigger.check_source("NotTheRightSource"))
        self.assertFalse(self.trigger_src.check_source("NotTheRightSource"))
        self.assertTrue(self.trigger_src.check_source("MockSource"))

    def test_fired_recently(self):
        self.trigger.check_condition(1)
        self.assertFalse(self.trigger.fired_recently())

        # If the trigger only just recently fired
        self.trigger.downtime = 1
        self.trigger.check_condition(0)
        self.trigger.update_last_time_fired()
        self.assertTrue(self.trigger.fired_recently())
        self.assertFalse(self.trigger.get_condition())

        # If the last fire time has happened a long time ago
        self.trigger.check_condition(0)
        self.trigger.get_last_time_fired = MagicMock(return_value=0)
        self.assertTrue(self.trigger.get_condition())

    def tearDown(self):
        self.trigger = None
        self.trigger_src = None


class TestDataChanged(unittest.TestCase):
    def setUp(self):
        config = {'class': 'monitor.trigger.data_changed.DataChanged', 'greater': 210, 'downtime': 10,
                  'level': 2, 'name': 'TestChangedTrigger'}
        self.trigger = DataChanged(config)

    def test_check_condition(self):
        self.assertFalse(self.trigger.check_condition(1))
        self.assertFalse(self.trigger.check_condition(1))
        self.assertTrue(self.trigger.check_condition(2))
        self.assertTrue(self.trigger.check_condition(1))

    def test_prepare_message(self):
        self.trigger.check_condition(0)
        self.assertIsInstance(self.trigger.prepare_message(), str)

    def tearDown(self):
        self.trigger = None


if __name__ == "__main__":
    unittest.main()

