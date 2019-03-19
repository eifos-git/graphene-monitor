from . import AbstractTrigger
from .utils import time_now, string_to_time
import logging


class EventOutdated(AbstractTrigger):
    """
    Event outdated is a trigger that fires every time the status of an event on the blockchain has a certain
    value at a given time after its' supposed start time.

        Example: If event x is still *upcoming* 10 minutes after its' start time, send me a warning.

    There are three values you can set in the config file:

        * time_window: acceptable delay in seconds (value for our example: 600)
        * status: status of the event (value for our example: upcoming)
        * explorer(optional): Has to be string with curly brackets. Send markdown links via telegram.

    When setting your parameters, please keep in mind that delay only gets checked every
    <monitor_interval> (defined in cli.py) seconds. This means that in a worst case scenario event is actually delayed
    monitor_interval + time_window seconds.
    """

    def __init__(self, config):
        super().__init__(config)
        self.outdated_events = []
        self._event_status = self.get_config("status", ignore=False)
        self._time_window = self.get_config("time_window", ignore=True, default=600)
        self._explorer = self.get_explorer()

    def get_status(self):
        """Retrieve what status has to be checked.
        """
        return self._event_status

    def get_time_window(self):
        return self._time_window

    def get_explorer(self):
        return self.get_config("explorer", ignore=True, default=None)

    def is_outdated(self, event):
        """Checks whether or not the event is outdated.
        Only ever says that an event is outdated when it currently is set to <event_status>
        """
        start_time = string_to_time(event["start_time"])
        timedelta = (time_now("datetime") - start_time).total_seconds()
        return timedelta > self.get_time_window() and event["status"] == self.get_status()

    def prepare_message(self):
        message = ""
        if len(self.outdated_events) is 1:
            message += "Outdated Event detected!\n"
        elif self._explorer:
            message = ""
        else:
            message += "Outdated Events detected!\n"

        message += "Trigger: {0}\n".format(self.get_config("name"))
        for event in self.outdated_events:
            if self._explorer:
                message += "Event Id: [{0}]({1})\n".format(event["event_id"], self._explorer.format(event["event_id"]))
            else:
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
