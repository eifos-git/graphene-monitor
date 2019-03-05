from . import AbstractTrigger
from datetime import datetime, timedelta
import logging


class EventOutdated(AbstractTrigger):
    def __init__(self, config):
        super().__init__(config)
        self.outdated_events = []
        self._event_status = self.get_config("status", ignore=False)
        self._time_window = self.get_config("time_window", ignore=True, default=600)

    def get_status(self):
        """Retrieve what status has to be checked.
        """
        return self._event_status

    def get_time_window(self):
        return self._time_window

    def is_outdated(self, event):
        """Checks whether or not the event is outdated.
        Only ever says that an event is outdated when it currently is set to <event_status>
        T"""
        start_time = datetime.strptime(event["start_time"], '%Y-%m-%dT%H:%M:%S')
        timedelta = (datetime.now() - start_time).total_seconds()
        return timedelta > self.get_time_window() and event["status"] == self.get_status()

    def prepare_message(self):
        message = ""
        if len(self.outdated_events) is 1:
            message += "Outdated Event detected!\n\n"
        else:
            message += "Outdated Events detected!\n\n"

        for event in self.outdated_events:
            message += "Event Id: {0}\n".format(event["event_id"])
        return message

    def check_condition(self, data):
        """Check whether one of the events' status is outdated.
        Outdated means that it should have been changed at least <time_window> seconds ago.
        time_window defaults to 600 seconds"""
        if self.get_status() is None:
            return False
        self.outdated_events.clear()
        for event in data:
            if self.is_outdated(event):
                # Event is upcoming but should already be in play
                self.outdated_events.append(event)
        return len(self.outdated_events) is not 0
