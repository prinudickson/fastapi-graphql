from graphene import Schema
from fastapi import FastAPI
from starlette_graphene3 import GraphQLApp, make_playground_handler
from app.db.database import Base, engine, SessionLocal
from app.db.data import prepare_database
from app.db.models import Employer, Job

from app.gql.queries import Query
from app.gql.mutations import Mutation

schema = Schema(query=Query, mutation=Mutation)

app = FastAPI()

@app.get("/employers")
def get_employers():
    session = SessionLocal()
    employers = session.query(Employer).all()
    session.close()
    return employers

@app.get("/jobs")
def get_jobs():
    session = SessionLocal()
    jobs = session.query(Job).all()
    session.close()
    return jobs

@app.on_event("startup")
def startup_event():
    prepare_database(SessionLocal, engine)

app.mount("/graphql", GraphQLApp(
    schema=schema,
    on_get=make_playground_handler()
))