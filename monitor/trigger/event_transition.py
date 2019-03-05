from . import AbstractTrigger
from .event_database import session, EventCache
from .utils import string_to_time, time_to_string, time_now


class EventTransition(AbstractTrigger):

    def prepare_message(self):
        data = self.get_data()
        message = "The following Event(s) have not changed for at least {0}seconds\n".format(self.get_time_window())
        for overdue_event in data:
            message += "Event Id: {0}\n".format(overdue_event["event_id"])
        return message

    def get_time_window(self):
        return self.get_config("time_window")

    def get_observe_start_time(self):
        # Do we care when the start time gets changed
        ost = self.get_config("observer_start_time", ignore=True, default=False)
        if not isinstance(ost, bool):
            ost = False
        return ost

    def check_condition(self, data):
        time_window = self.get_time_window()
        observe_start_time = self.get_observe_start_time()
        events_overdue = []

        def check_existing_has_to_fire(event, entry):
            """Entry already exists in the database. Check if it has changed
            if it has changed: No trigger should be ired
            if it hasnt changed: If the time window is already over, fire
            """
            if event["status"] != entry.status or (event["start_time"] != string_to_time(entry.start_time) and observe_start_time):
                # status has changed
                entry.status = event["status"]
                entry.start_time = event["start_time"]
                entry.last_time_changed = time_to_string(time_now())
            else:
                if (time_now() - string_to_time(entry.last_time_changed)).total_seconds() > time_window:
                    return True
            return False

        def add_new(event):
            x = EventCache()
            x.event_id = event["event_id"]
            x.start_time = event["start_time"]
            x.status = event["status"]
            x.last_time_changed = time_to_string(time_now())
            session.add(x)

        for event in data:
            entry = (
                session.query(EventCache)
                .filter_by(event_id=event["event_id"])
                .first()
            )
            if entry is not None:
                if check_existing_has_to_fire(event, entry):
                    events_overdue.append(event)
            else:
                add_new(event)
        session.commit()
        self.update_data(new_data=events_overdue)
        print("len gevent" + str(len(events_overdue)))
        return len(events_overdue) != 0
