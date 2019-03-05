import unittest
import sys
import logging
import mock
from io import StringIO
from monitor import Config, setup_monitors
from.fixtures import fixture_data,lookup, config, receive_incident, reset_storage
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from monitor.trigger.event_outdated import EventOutdated
from monitor.action import stdout
import copy


class TestEvent(unittest.TestCase):
    def setUp(self):
        fixture_data()
        lookup.clear()
        self.storage = reset_storage()

        Config.add_general_config(dict(config="test/test_event_outdated.yaml", trigger_downtime=0))
        Config.load_monitor_config()
        self.monitors = setup_monitors()[0]
        # keep track of the events that get returned
        self.ret_len = 0
        self.action_func = copy.copy(stdout.Stdout.fire)

    def side_effect(self, message):
        """
        :return: Amount of events that fired
        """
        # The actual length is 4 lines longer to make it easier for humans to read

        self.ret_len = len(message.split("\n")) - 4
        #self.action_func(self, message)

    def test_event_outdated(self):
        mock = MagicMock(return_value=None)
        mock.side_effect = self.side_effect
        stdout.Stdout.fire = mock

        self.monitors.do_monitoring()
        # ret len is the string that gets printed. 6 means there are exactly 2 events that fired
        # Dependant on prepare message
        self.assertEqual(2, self.ret_len)

    def test_event_not_outdated(self):
        # Every Event is outdated
        mockIsOutdated = MagicMock(return_value=False)
        old_is_outdated = copy.copy(EventOutdated._is_outdated)
        EventOutdated._is_outdated = mockIsOutdated

        # Count and catch action.fire operations
        mockFire = MagicMock(return_value=None)
        mockFire.side_effect = self.side_effect
        stdout.Stdout.fire = mockFire

        self.monitors.do_monitoring()
        self.assertEqual(0, self.ret_len)

        #Set is_outdated to the original functionality
        EventOutdated._is_outdated = old_is_outdated

    def retrieve_data_sideeffect(self):
        self.monitors.sources[0]._data = self.data

    def test_event_changed(self):
        from monitor.source.peerplays_events import PeerplaysEvents
        now = (datetime.now()-timedelta()).strftime('%Y-%m-%dT%H:%M:%S')
        # negative time added is like starting the monitor in the future
        future = (datetime.now()-timedelta(seconds=610)).strftime('%Y-%m-%dT%H:%M:%S')
        self.data = [dict(event_id="1.22.1", start_time=now, status="upcoming"),
                     dict(event_id="1.22.2", start_time=now, status="upcoming")]
        # retrieve some predefined data
        mock_retrieve_data = MagicMock()
        mock_retrieve_data.side_effect = self.retrieve_data_sideeffect
        old_retrieve_data = copy.copy(PeerplaysEvents.retrieve_data)
        PeerplaysEvents.retrieve_data = mock_retrieve_data
        # counting instead of firering the trigger
        mock = MagicMock(return_value=None)
        mock.side_effect = self.side_effect
        stdout.Stdout.fire = mock

        self.monitors.do_monitoring()
        self.assertEqual(0, self.ret_len)
        self.ret_len = 0

        # Jump six minutes and ten seconds in the future
        self.data = [dict(event_id="1.22.1", start_time=future, status="upcoming"),
                     dict(event_id="1.22.2", start_time=future, status="upcoming")]
        self.monitors.do_monitoring()
        self.assertEqual(2, self.ret_len)

        PeerplaysEvents.retrieve_data = old_retrieve_data

    def tearDown(self):
        self.ret_len = 0
        self.monitors = None
        Config.data = list()


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    unittest.main()
