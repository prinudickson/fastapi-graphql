from sqlalchemy import create_engine, Column, Integer, String as sqString, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_USER = "postgres"
DATABASE_PASSWORD = "admin"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"
DATABASE_NAME = "fastapi_graphene"

DB_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(DB_URL, pool_size=50, max_overflow=5)
conn = engine.connect()

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
