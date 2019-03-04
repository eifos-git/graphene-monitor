from peerplays.sport import Sports
from peerplays.eventgroup import EventGroups
from peerplays.event import Events
from peerplays.exceptions import EventDoesNotExistException
from peerplaysapi.exceptions import UnhandledRPCError
import logging
from . import AbstractSource


class PeerplaysEvents(AbstractSource):
    def __init__(self, source_config, source_name):
        super().__init__(source_config, source_name)
        self.sport_id = None
        self.eventgroup_id = None
        self._get_additional_config()

    def _get_additional_config(self):
        self.sport_id = super()._get_config_value("sport_id", ignore_key_error=True)
        if self.sport_id is not None:
            self.eventgroup_id = super()._get_config_value("eventgroup_id", ignore_key_error=True)

    def _append_event(self, data, event):
        data.append(dict(event_id=event["id"], start_time=event["start_time"], status=event["status"]))

    def retrieve_data(self):
        """Depending on your config file returns all the events of the blockchain as a list of dicts"""
        self._set_data()
        data = []

        if self.sport_id is None and self.eventgroup_id is None:
            # no sport id is given, therefore we want to check all events
            for sport in Sports():
                for eventgroup in EventGroups(sport["id"]):
                    for event in Events(eventgroup["id"]):
                        self._append_event(data, event)

        elif self.eventgroup_id is None:
            # no eventgroup id is given, therefore we check all of the sports events
            try:
                eventgroups = EventGroups(self.sport_id)
            except UnhandledRPCError:
                logging.warning("Unhandled RPC Error in {0} for sport id. Sport ids have to start with 1.20.<>"
                                .format(self.get_source_name()))
                return
            for eventgroup in eventgroups:
                for event in Events(eventgroup["id"]):
                    self._append_event(data, event)

        # Eventgroup id given, only check its' events
        else:
            try:
                events = Events(self.eventgroup_id)
            except UnhandledRPCError:
                logging.warning("Unhandled RPC Error in {0} for event id. Eventgroup ids have start with 1.21.<>"
                                .format(self.get_source_name()))
            for event in Events(self.eventgroup_id):
                self._append_event(data, event)

        self._set_data(data)






