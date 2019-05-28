import re
from . import AbstractTrigger
from .trigger_db import EventCacheDatabase
from datetime import datetime
from .utils import string_to_time, time_to_string, time_now


class DuplicateEvent(AbstractTrigger):
    """
    Duplicate Event is a Trigger that is supposed to fire whenever Duplicate Events appear on the Blockchain.
    This is determined by looking at the name of an Event.
    This Trigger doesn't differ between home and away teams, hence we have to seperate the match into it's two parts.
    Due to a missing convention about the separator between the two teams of a match, possible separation characters
    have to be provided in the config file.

    Available Config settings are:
        * seperator: Example: ".| . | @ | v |". Standard Python regular Expression Syntax. Seperate each seperator
        with |
        * time_window: How much time can be between two Events with the same teams in seconds
    """
    def __init__(self, config):
        super().__init__(config)
        if self.get_clean():
            EventCacheDatabase.clear_all()
        self._time_window = self.get_config("time_window", ignore=True, default=21600)
        self._seperators = self.get_config("seperators", ignore=False)

    def get_clean(self):
        return self.get_config("clean", ignore=True, default="True")

    def get_time_window(self):
        return self._time_window

    def get_seperators(self):
        return self._seperators



    def check_condition(self, data):
        database = EventCacheDatabase

        time_window = self.get_time_window()
        t_now = time_now()
        events_duplicate = []

        def check_event_is_duplicate(event):
            event_name = event["name"]
            teams = re.split(self._seperators, event_name)
            if len(teams != 2):
                # TODO error handling
                print("Something went wrong during the seperation of event name")
                return False

            for event in database.query.all():
                db_teams= re.split(self.get_seperators(), event.event_name)
                if teams[0] not in db_teams or teams[1] not in db_teams:
                    return False

            if (t_now - entry.start_time).seconds >= time_window:
                return False
            return True

        for event in data:
            entry = database.get_event(event["event_id"])
            if entry is not None:
                # entry exists by id therefore we only have to think about deleting it
                if (t_now - entry.start_time).seconds >= time_window:
                    # events is to old to possibly fire
                    database.remove(event["event_id"])
            else:
                if check_event_is_duplicate(event):
                    events_duplicate.append(event)
                else:
                    database.add(event)

