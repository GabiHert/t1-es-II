from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://user:password@localhost:5432/mydatabase"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()