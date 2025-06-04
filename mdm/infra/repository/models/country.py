from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from config.db.alembic.base import Base


class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String, nullable=False)
    numeric_code = Column(Integer, nullable=False)
    capital_city = Column(String, nullable=False)
    population = Column(BigInteger, nullable=False)
    area = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    currencies = relationship("Currency", back_populates="country", cascade="all, delete-orphan")

