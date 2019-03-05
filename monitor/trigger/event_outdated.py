from . import AbstractTrigger
from datetime import datetime, timedelta
import logging


class EventOutdated(AbstractTrigger):
    def __init__(self, config):
        super().__init__(config)
        self.outdated_events = []

    @staticmethod
    def _is_outdated(time_window, event):
        start_time = datetime.strptime(event["start_time"], '%Y-%m-%dT%H:%M:%S')
        timedelta = (datetime.now() - start_time).total_seconds()
        return timedelta > time_window and event["status"] == "upcoming"

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
        self.outdated_events.clear()
        time_window = self.get_config("time_window", ignore=True)
        if time_window is None:
            time_window = 600
        for event in data:
            if EventOutdated._is_outdated(time_window, event):
                # Event is upcoming but should already be in play
                self.outdated_events.append(event)
        return len(self.outdated_events) is not 0


