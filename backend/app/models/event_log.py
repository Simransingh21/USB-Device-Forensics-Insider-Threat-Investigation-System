from sqlalchemy import Column, Integer, String, DateTime

from app.database.database import Base


class EventLog(Base):

    __tablename__ = "event_logs"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(Integer)

    source = Column(String)

    timestamp = Column(String)

    scan_id = Column(Integer)