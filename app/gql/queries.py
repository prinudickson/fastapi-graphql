from graphene import ObjectType, List
from app.gql.types import JobObject, EmployerObject
from app.db.data import jobs_data, employers_data
from app.db.database import SessionLocal
from app.db.models import Employer, Job
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(root, info):
        session = SessionLocal()
        jobs = session.query(Job).options(joinedload(Job.employer)).all()
        session.close()
        return jobs
        #return SessionLocal().query(Job).all()
    
    @staticmethod
    def resolve_employers(root, info):
        session = SessionLocal()
        # employers = session.query(Employer).all()
        employers = session.query(Employer).options(joinedload(Employer.jobs)).all()
        session.close()
        return employers
        #return SessionLocal().query(Employer).all() 
