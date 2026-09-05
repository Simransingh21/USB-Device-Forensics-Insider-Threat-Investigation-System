from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)

    start_time = Column(DateTime, default=datetime.utcnow)

    end_time = Column(DateTime, nullable=True)

    status = Column(String, default="Running")

    total_artifacts = Column(Integer, default=0)