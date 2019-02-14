import unittest
from unittest.mock import MagicMock
import logging
import os
from monitor import Monitor
from test import MockBuffer, MockTrigger, MockAction

config = {'sources': [{'MockBuffer': {'class': 'test.MockBuffer'}}],
          'triggers': [{'MockTrigger':
                        {'class': 'test.MockTrigger',
                            'source': 'MockBuffer', 'level': 0}}],
          'actions': [{'action': {'class': 'monitor.action.stdout.Stdout', 'level': 0}}]}


class TestMonitorSetup(unittest.TestCase):
    def setUp(self):
        global config
        self.monitor = Monitor(config, name="integration_test", general_config=dict())
        self.monitor.st_pairs[0].trigger.fired_recently = MagicMock(return_value=False)

    def update_condition_data(self):
        return self.monitor.st_pairs[0].source.get_data(), self.monitor.st_pairs[0].trigger.fire_condition_met

    def test_do_monitoring(self):
        self.monitor.do_monitoring()
        data, condition = self.update_condition_data()
        self.assertTrue((data == 0) and (condition is True))

        # No trigger downtime set
        self.monitor.do_monitoring()
        data, condition = self.update_condition_data()
        self.assertTrue((data == 0) and (condition is True))

        self.monitor.do_monitoring()
        data, condition = self.update_condition_data()
        self.assertTrue((data == 1) and (condition is False))

        self.monitor.do_monitoring()
        data, condition = self.update_condition_data()
        self.assertTrue(data is None)



if __name__ == '__main__':
    log = logging.getLogger(__name__)
    unittest.main()
