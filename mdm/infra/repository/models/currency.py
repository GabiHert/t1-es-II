from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.db.alembic.base import Base


class Currency(Base):
    __tablename__ = 'currencies'

    currency_id = Column(Integer, primary_key=True)
    currency_code = Column(String, nullable=False)
    currency_name = Column(String, nullable=False)
    currency_symbol = Column(String, nullable=False)
    country_id = Column(Integer, ForeignKey('countries.country_id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    country = relationship("Country", back_populates="currencies")