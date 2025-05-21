from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True)
    country_name = Column(String, nullable=False)
    numeric_code = Column(Integer, nullable=False)
    capital_city = Column(String, nullable=False)
    population = Column(Integer, nullable=False)
    area = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    currencies = relationship("Currency", back_populates="country")

