from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class EventCache(Base):
    __tablename__ = "datacache"
    id = Column(Integer, primary_key=True)
    event_id = Column(String(50))
    start_time = Column(String(50))
    last_time_changed = Column(String(50))
    status = Column(String(50))

    def __repr__(self):
        return "Event: {0} - Status: {1} - Changetime: {2}".format(self.event_id, self.status, self.last_time_changed)

engine = create_engine("sqlite:///data_monitor.sqlite", echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()