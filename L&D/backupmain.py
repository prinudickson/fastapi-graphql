from graphene import Schema, ObjectType, List, Field, String, Int, Float
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_graphiql_handler, make_playground_handler
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

class Employer(Base):
    __tablename__="employers"

    id = Column(Integer, primary_key=True)
    name = Column(sqString)
    contact_email = Column(sqString)
    industry = Column(sqString)
    jobs = relationship("Job", back_populates="employer")

class Job(Base):
    __tablename__="jobs"

    id = Column(Integer, primary_key=True)
    title = Column(sqString)
    description = Column(sqString)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship("Employer", back_populates="jobs")

Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



employers_data = [
    {"id": 1, "name": "MetaTechA", "contact_email": "contact@company-a.com", "industry": "Tech"},
    {"id": 2, "name": "MoneySoftB", "contact_email": "contact@company-b.com", "industry": "Finance"},
]

jobs_data = [
    {"id": 1, "title": "Software Engineer", "description": "Develop web applications", "employer_id": 1},
    {"id": 2, "title": "Data Analyst", "description": "Analyze data and create reports", "employer_id": 1},
    {"id": 3, "title": "Accountant", "description": "Manage financial records", "employer_id": 2},
    {"id": 4, "title": "Manager", "description": "Manage people who manage records", "employer_id": 2},
]



def prepare_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session = SessionLocal()

    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        jb = Job(**job)
        session.add(jb)  

    session.commit()
    session.close()

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
        return [job for job in jobs_data if job["employer_id"] == root["id"]]

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        return next((employer for employer in employers_data if employer["id"] == root["employer_id"]), None)


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(self, info):
        return jobs_data
    
    @staticmethod
    def resolve_employers(self, info):
        return employers_data 

schema = Schema(query=Query)

app = FastAPI()

@app.on_event("startup")
def startup_event():
    prepare_database()

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))