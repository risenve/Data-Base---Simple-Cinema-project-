from sqlalchemy import Column, Integer, String, Boolean, Numeric
from sqlalchemy.orm import relationship

from app.database import Base


class Correspondent(Base):
    __tablename__ = "correspondents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    specification = Column(String(50), nullable=False)
    operator = Column(Boolean, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    reportages = relationship(
        "Reportage",
        back_populates="correspondent",
        cascade="all, delete",
    )