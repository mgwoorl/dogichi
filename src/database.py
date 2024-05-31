from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///db1.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseDBModel = declarative_base()
