from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from app.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    place = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)
    danger = Column(String(50), nullable=False)
    type = Column(String(100), nullable=False)

    reportages = relationship(
        "Reportage",
        back_populates="event",
        cascade="all, delete",
    )