from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:password@localhost:5432/online_store'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base = declarative_base()
