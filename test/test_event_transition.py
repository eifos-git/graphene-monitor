import unittest
import time
from unittest.mock import MagicMock
from monitor import Config, Monitor
from monitor.source.peerplays_events import PeerplaysEvents
from monitor.trigger.trigger_db import EventCacheDatabase
from monitor.action.stdout import Stdout

general_config = {"config": "mock.config", "monitor_interval": 0, "multithreading": False, "trigger_downtime": 0}

config = {'sources': [{'MockBuffer': {'class': "monitor.source.peerplays_events.PeerplaysEvents"}}],
          'triggers': [{'event_transition_delayed':
                        {'class': 'monitor.trigger.event_transition.EventTransition',
                         'time_window': 1,
                         'observe_start_time': True,
                         'level': 0
                        }}],
          'actions': [{'action': {'class': 'monitor.action.stdout.Stdout', 'level': 0}}]}

# config2 == config + 'status': 'in_progress'
config2 = {'sources': [{'MockBuffer': {'class': "monitor.source.peerplays_events.PeerplaysEvents"}}],
          'triggers': [{'event_transition_delayed':
                        {'class': 'monitor.trigger.event_transition.EventTransition',
                         'status': 'in_progress',
                         'time_window': 1,
                         'observe_start_time': True,
                         'level': 0
                        }}],
          'actions': [{'action': {'class': 'monitor.action.stdout.Stdout', 'level': 0}}]}


class TestEventTransition(unittest.TestCase):

    def setUp(self):
        # Empty Database
        EventCacheDatabase.clear_all()

        mock = MagicMock()
        mock.side_effect = self.retrieve_data_mock
        PeerplaysEvents.retrieve_data = mock

        action_mock = MagicMock(return_value=None)
        action_mock.side_effect = self.action_message_mock
        Stdout.fire = action_mock

    def retrieve_data_mock(self):
        data = None
        if self.iteration == 0:
            data = [{'event_id': '1.22.1', 'start_time': '2019-01-20T12:00:00', 'status': 'in_progress'},
                    {'event_id': '1.22.2', 'start_time': '2019-01-21T12:00:00', 'status': 'in_progress'},
                    {'event_id': '1.22.3', 'start_time': '2019-01-22T12:00:00', 'status': 'upcoming'},
                    {'event_id': '1.22.4', 'start_time': '2029-01-23T12:00:00', 'status': 'upcoming'}]
        elif self.iteration == 1:
            data = [{'event_id': '1.22.1', 'start_time': '2019-01-20T12:00:00', 'status': 'finished'},  # finished
                    {'event_id': '1.22.2', 'start_time': '2019-01-21T12:00:00', 'status': 'in_progress'},  # Not Changed
                    {'event_id': '1.22.3', 'start_time': '2019-02-22T12:00:00', 'status': 'upcoming'},  # s_t changed
                    {'event_id': '1.22.4', 'start_time': '2029-01-23T12:00:00', 'status': 'upcoming'},
                    {'event_id': '1.22.5', 'start_time': '2019-01-24T12:00:00', 'status': 'upcoming'}]
        self.iteration += 1
        # set data internally
        self.monitor.sources[0]._set_data(data)

    def action_message_mock(self, message):
        # Every event is printed in a newline, 2 lines are "metadata"
        self.event_amount = len(message.split("\n")) - 3

    def test_database_setup(self):
        Config.add_general_config(general_config)
        self.monitor = Monitor(config, name="integration_test", general_config=dict())
        self.iteration = 0

        self.monitor.do_monitoring()

        #sleep 2 seconds so the time window is already reached
        time.sleep(2)
        self.monitor.do_monitoring()
        self.assertEqual(EventCacheDatabase.session
                         .query(EventCacheDatabase.EventCache)
                         .count(), 5)  # only one new event
        self.assertEqual(self.event_amount, 2)

    def test_event_transition_with_status(self):
        Config.add_general_config(general_config)
        self.monitor = Monitor(config2, name="integration_test", general_config=dict())
        self.iteration = 0

        self.monitor.do_monitoring()

        # sleep 2 seconds so the time window is already reached
        time.sleep(2)
        self.monitor.do_monitoring()
        self.assertEqual(EventCacheDatabase.session
                         .query(EventCacheDatabase.EventCache)
                         .count(), 5)  # only one new event
        # Event 1.22.4 doesnt matter because we dont care about upcoming events
        self.assertEqual(self.event_amount, 1)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
