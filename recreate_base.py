
import sys
sys.path.insert(0, '.')

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

# Создать НОВУЮ Base
Base = declarative_base()

# Переопределить модели с новой Base
class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True, index=True)
    place = Column(String(100))
    city = Column(String(100))
    date = Column(Date)
    duration = Column(Integer)
    danger = Column(String(50))
    type = Column(String(100))
    extra_metadata = Column(JSONB, nullable=True)
    reportages = relationship("Reportage", back_populates="event")

class Correspondent(Base):
    __tablename__ = "correspondent"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    country = Column(String(50))
    city = Column(String(50))
    specification = Column(String(50))
    operator = Column(Boolean)
    price = Column(Numeric(10, 2))
    reportages = relationship("Reportage", back_populates="correspondent")

class Reportage(Base):
    __tablename__ = "reportage"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    quality = Column(String(50))
    time = Column(Time)
    video = Column(Boolean)
    event_id = Column(Integer, ForeignKey("events.id"))
    correspondent_id = Column(Integer, ForeignKey("correspondent.id"))
    event = relationship("Event", back_populates="reportages")
    correspondent = relationship("Correspondent", back_populates="reportages")

print("✅ New Base created with fresh models")

# Проверить
print(f"Event columns: {[c.name for c in Event.__table__.columns]}")
print(f"Has extra_metadata: {'extra_metadata' in Event.__table__.c}")
