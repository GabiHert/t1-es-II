from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv('DATABASE_URL', "postgresql://mdm_user:mdm_password@localhost:5434/mdm_database")

engine = create_engine(DATABASE_URL)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()