from sqlalchemy import Column, Integer, String

from app.database.database import Base


class Finding(Base):

    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)

    scan_id = Column(Integer)

    severity = Column(String)

    title = Column(String)

    description = Column(String)

    timestamp = Column(String)