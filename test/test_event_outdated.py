import unittest
from monitor.source.peerplays_events import PeerplaysEvents
import sys
import logging
import mock
from io import StringIO
from monitor import Config, setup_monitors, Monitor
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from monitor.trigger.event_outdated import EventOutdated
from monitor.action import stdout
import copy

config = {'sources': [{'MockBuffer': {'class': "monitor.source.peerplays_events.PeerplaysEvents"}}],
          'triggers': [{'upcoming_event_outdated':
                        {'class': 'monitor.trigger.event_outdated.EventOutdated',
                         'time_window': 600,
                         'status': 'upcoming',
                         'level': 0
                        }}],
          'actions': [{'action': {'class': 'monitor.action.stdout.Stdout', 'level': 0}}]}


class TestEvent(unittest.TestCase):
    def setUp(self):
        Config.add_general_config(dict(trigger_downtime=0))
        self.monitors = Monitor(config, name="event_outdated_test", general_config=dict())
        # keep track of the events that get returned
        self.ret_len = 0
        self.action_func = copy.copy(stdout.Stdout.fire)

        # Mock function for retrieve data
        mock_retrieve_data = MagicMock()
        mock_retrieve_data.side_effect = self.retrieve_data_sideeffect
        PeerplaysEvents.retrieve_data = mock_retrieve_data

        # Mock function instead of stdout print
        mock = MagicMock(return_value=None)
        mock.side_effect = self.side_effect
        stdout.Stdout.fire = mock

    def side_effect(self, message):
        """
        :return: Amount of events that fired
        """
        # The actual length is 4 lines longer to make it easier for humans to read

        self.ret_len = len(message.split("\n")) - 4
        # self.action_func(self, message)

    def retrieve_data_sideeffect(self):
        self.monitors.sources[0]._data = self.data

    def test_event_changed(self):
        now = (datetime.utcnow()-timedelta()).strftime('%Y-%m-%dT%H:%M:%S')
        future = (datetime.utcnow()-timedelta(seconds=610)).strftime('%Y-%m-%dT%H:%M:%S')
        self.data = [dict(event_id="1.22.1", start_time=now, status="upcoming"),
                     dict(event_id="1.22.2", start_time=now, status="upcoming")]
        self.monitors.do_monitoring()
        self.assertEqual(0, self.ret_len)

        self.data = [dict(event_id="1.22.1", start_time=future, status="in-progress"),
                     dict(event_id="1.22.2", start_time=future, status="in-progress")]
        self.monitors.do_monitoring()
        self.assertEqual(0, self.ret_len)

    def test_event_not_changed(self):
        now = (datetime.utcnow() - timedelta()).strftime('%Y-%m-%dT%H:%M:%S')
        future = (datetime.utcnow() - timedelta(seconds=610)).strftime('%Y-%m-%dT%H:%M:%S')
        self.data = [dict(event_id="1.22.1", start_time=now, status="upcoming"),
                     dict(event_id="1.22.2", start_time=now, status="upcoming")]
        self.monitors.do_monitoring()
        self.assertEqual(0, self.ret_len)

        self.data = [dict(event_id="1.22.1", start_time=future, status="upcoming"),
                     dict(event_id="1.22.2", start_time=future, status="upcoming")]
        self.monitors.do_monitoring()
        self.assertEqual(2, self.ret_len)

    def test_wrong_status(self):
        # event is outdated, but we are not looking for in-progress events
        now = (datetime.utcnow() - timedelta()).strftime('%Y-%m-%dT%H:%M:%S')
        future = (datetime.utcnow() - timedelta(seconds=610)).strftime('%Y-%m-%dT%H:%M:%S')
        self.data = [dict(event_id="1.22.1", start_time=now, status="in-progress")]
        self.monitors.do_monitoring()
        self.assertEqual(0, self.ret_len)

        self.data = [dict(event_id="1.22.1", start_time=future, status="in-progress")]
        self.monitors.do_monitoring()
        self.assertEqual(0, self.ret_len)

    def tearDown(self):
        self.ret_len = 0
        self.monitors = None
        Config.data = list()


if __name__ == '__main__':
    log = logging.getLogger(__name__)
    unittest.main()
