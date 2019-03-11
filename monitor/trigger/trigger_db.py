from . import AbstractDatabase
from .utils import time_now, time_to_string
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker



class EventCacheDatabase(AbstractDatabase):
    Base = declarative_base()

    class EventCache(Base):
        __tablename__ = "datacache"
        id = Column(Integer, primary_key=True)
        event_id = Column(String(50))
        start_time = Column(String(50))
        last_time_changed = Column(String(50))
        status = Column(String(50))

        def __repr__(self):
            return "Event: {0} - Status: {1} - Changetime: {2}"\
                .format(self.event_id, self.status, self.last_time_changed)

    engine = create_engine("sqlite:///event_cache.sqlite", echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    @staticmethod
    def clear_all():
        x = EventCacheDatabase.session.query(EventCacheDatabase.EventCache).first()
        while x is not None:
            EventCacheDatabase.session.delete(x)
            x = EventCacheDatabase.session.query(EventCacheDatabase.EventCache).first()

    @staticmethod
    def _get(column, column_value):
        return EventCacheDatabase.session.query(EventCacheDatabase.EventCache)\
            .filter_by(column=column_value)\
            .first()

    @staticmethod
    def add(event):
        x = EventCacheDatabase.EventCache()
        x.event_id = event["event_id"]
        x.start_time = event["start_time"]
        x.status = event["status"]
        x.last_time_changed = time_to_string(time_now())
        EventCacheDatabase.session.add(x)

    @staticmethod
    def get_event(event_id):
        return EventCacheDatabase.session.query(EventCacheDatabase.EventCache)\
            .filter_by(event_id=event_id)\
            .first()
