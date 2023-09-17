import os
from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, Integer, String as sqString, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
#from app.settings.config import *

load_dotenv()

DB_URL = f"postgresql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
engine = create_engine(DB_URL, pool_size=50, max_overflow=5, echo=True)
conn = engine.connect()

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
