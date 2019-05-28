from peerplays.sport import Sports
from peerplays.eventgroup import EventGroups
from peerplays.event import Events
from peerplays.exceptions import EventDoesNotExistException
from peerplaysapi.exceptions import UnhandledRPCError
import logging
from . import AbstractSource
from graphenecommon.instance import SharedInstance


class PeerplaysEvents(AbstractSource):
    """Retrieves a list of all events on the peerplays blockchain with its status and start_time.

    Available config settings are:

        * sport_id (optional): 1.20.<id>
        * eventgroup_id (optional): 1.21.<id>
        * node (optional): list of nodes to connect to. Takes 2nd node if 1st node is unavailable.

    **Returns** list of dictionaries with the following keys:

        * event_id: Event identifier
        * start_time: Supposed start time of the event
        * status: Current status.

    Please note that all events are handled as if they were one source. This can lead to unexpected trouble when
    activating trigger downtime e.g. one trigger fired for event 1.22.1 trigger downtime is activated for 20 minutes
    and now event 1.22.10 is supposed to fire, but doesn't for 20 minutes.
    One possible workaround is to deactivate trigger downtime.
    If you don't want to get spammed, we recommend to create separate event sources for sports/eventgroups
    """
    def __init__(self, source_config, source_name):
        super().__init__(source_config, source_name)
        SharedInstance.config = dict(node=self._get_node_list())
        self.sport_id = None
        self.eventgroup_id = None
        self._get_additional_config()

    def _get_node_list(self):
        return self.get_config("node")

    def _get_additional_config(self):
        self.sport_id = super().get_config("sport_id", ignore_key_error=True)
        self.eventgroup_id = super().get_config("eventgroup_id", ignore_key_error=True)

    def _append_event(self, data, event):
        data.append(dict(event_id=event["id"], start_time=event["start_time"], status=event["status"], name=event["name"]))

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

        # sport id is given: only check its' events
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

        # Eventgroup id is given: only check its' events
        else:
            try:
                events = Events(self.eventgroup_id)
            except UnhandledRPCError:
                logging.warning("Unhandled RPC Error in {0} for event id. Eventgroup ids have start with 1.21.<>"
                                .format(self.get_source_name()))
            for event in events:
                self._append_event(data, event)

        self._set_data(data)






