from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://dem_user:dem_password@localhost:5433/dem_database')

engine = create_engine(DATABASE_URL)
db_session = scoped_session(sessionmaker(autocommit=False,
                                       autoflush=False,
                                       bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    # Import models here to avoid circular imports
    from infra.repositories.models import Extraction, Load
    Base.metadata.create_all(bind=engine) 