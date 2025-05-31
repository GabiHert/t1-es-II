from datetime import datetime
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from config.database import Base

class Extraction(Base):
    __tablename__ = 'extractions'

    extraction_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    loads = relationship("Load", back_populates="extraction")

class Load(Base):
    __tablename__ = 'loads'

    load_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    extraction_id = Column(UUID(as_uuid=True), ForeignKey('extractions.extraction_id'))
    source = Column(String, nullable=False)
    service = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, nullable=False)
    extraction = relationship("Extraction", back_populates="loads") 