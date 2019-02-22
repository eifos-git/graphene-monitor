from peerplays.sport import Sports
from peerplays.eventgroup import EventGroups
from peerplays.event import Events
from peerplays.exceptions import EventDoesNotExistException
from . import AbstractSource


class PeerplaysEvents(AbstractSource):
    def __init__(self, source_config, source_name):
        super().__init__(source_config, source_name)
        self.counter = -1

    def increment(self):
        self.counter += 1
        return "1.22." + str(self.counter)

    def retrieve_data(self):
        data = []
        for sport in Sports():
            for eventgroup in EventGroups(sport["id"]):
                for event in Events(eventgroup["id"]):
                    data.append(dict(start_time=event["start_time"], status=event["status"]))
        return data


