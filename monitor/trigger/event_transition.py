from . import AbstractTrigger
from .trigger_db import EventCacheDatabase
from .utils import string_to_time, time_to_string, time_now


class EventTransition(AbstractTrigger):
    """Event Transition is a trigger that makes sure, that an Event changes it's status (or if desired start_time)
    after at least <time_window>seconds.
    Internally all the events are saved as a sqlalchemy database.

    All possibly configurations the user can set are:

        * time_window: acceptable delay in seconds
        * status: Only Events can trigger an action
        * clean (default=True): The Database of events is emptied before we start monitoring

    When setting your parameters please keep it mind that delay only gets checked every
    <monitor_interval> (defined in cli.py) seconds. This means that in a worst case scenario event is actually delayed
    monitor_interval + time_window seconds.
    """
    def __init__(self, config):
        super().__init__(config)
        if self.get_clean():
            EventCacheDatabase.clear_all()

    def prepare_message(self):
        data = self.get_data()
        message = "The following Event(s) have not changed for at least {0} seconds\n".format(self.get_time_window())
        for overdue_event in data:
            message += "Event Id: {0}\n".format(overdue_event["event_id"])
        return message

    def get_time_window(self):
        return self.get_config("time_window")

    def get_status_to_look_for(self):
        return self.get_config("status", ignore=True)

    def get_clean(self):
        return self.get_config("clean", ignore=True, default="True")

    def get_observe_start_time(self):
        # Do we care when the start time gets changed
        ost = self.get_config("observe_start_time", ignore=True, default=False)
        if not isinstance(ost, bool):
            ost = False
        return ost

    def check_condition(self, data):
        time_window = self.get_time_window()
        observe_start_time = self.get_observe_start_time()
        events_overdue = []
        database = EventCacheDatabase

        def check_existing_has_to_fire(event, entry):
            """Entry already exists in the database. Check if it has changed
            if it has changed: No trigger should be ired
            if it hasnt changed: If the time window is already over, fire
            """
            if event["status"] != entry.status or (event["start_time"] != entry.start_time and observe_start_time):
                # status has changed
                entry.status = event["status"]
                entry.start_time = event["start_time"]
                entry.last_time_changed = time_to_string(time_now())
            else:
                if (time_now() - string_to_time(entry.last_time_changed)).total_seconds() > time_window:
                    return True
            return False

        for event in data:
            entry = database.get_event(event["event_id"])
            if entry is not None:
                if check_existing_has_to_fire(event, entry):
                    status_tlf = self.get_status_to_look_for()
                    # If the user defines status for the trigger, only events with that status should fire
                    if status_tlf is None or event["status"] == status_tlf:
                        events_overdue.append(event)
            else:
                database.add(event)

        database.session.commit()
        self.update_data(new_data=events_overdue)
        return len(events_overdue) != 0
