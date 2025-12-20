from sqlalchemy import Column, Integer, String, Date, Time, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Reportage(Base):
    __tablename__ = "reportages"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    quality = Column(String(50), nullable=False)
    time = Column(Time, nullable=False)
    video = Column(Boolean, nullable=False)

    event_id = Column(
        Integer,
        ForeignKey("events.id", ondelete="CASCADE"),
        nullable=False,
    )
    correspondent_id = Column(
        Integer,
        ForeignKey("correspondents.id", ondelete="CASCADE"),
        nullable=False,
    )

    event = relationship("Event", back_populates="reportages")
    correspondent = relationship("Correspondent", back_populates="reportages")