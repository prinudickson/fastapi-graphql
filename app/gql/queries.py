from graphene import ObjectType, List, Field, Int
from app.gql.types import JobObject, EmployerObject, UserObject, JobApplicationObject
from app.db.database import SessionLocal
from app.db.models import Employer, Job, User, JobApplication
from sqlalchemy.orm import joinedload


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    jobapplications = List(JobApplicationObject)

    @staticmethod
    def resolve_jobs(root, info):
        session = SessionLocal()
        #jobs = session.query(Job).options(joinedload(Job.employer)).all()
        jobs = session.query(Job).all()
        session.close()
        return jobs
    
    @staticmethod
    def resolve_job(root, info, id: int):
        session = SessionLocal()
        jb = session.query(Job).filter(Job.id == id).first()
        session.close()
        return jb
    
    @staticmethod
    def resolve_employers(root, info):
        session = SessionLocal()
        employers = session.query(Employer).all()
        # employers = session.query(Employer).options(joinedload(Employer.jobs)).all()
        session.close()
        return employers

    @staticmethod
    def resolve_employer(root, info, id: int):
        session = SessionLocal()
        em = session.query(Employer).filter(Employer.id == id).first()
        session.close()
        return em

    @staticmethod
    def resolve_users(root, info):
        session = SessionLocal()
        users = session.query(User).all()
        # employers = session.query(Employer).options(joinedload(Employer.jobs)).all()
        session.close()
        return users

    @staticmethod
    def resolve_jobapplications(root, info):
        session = SessionLocal()
        jobapplications = session.query(JobApplication).all()
        session.close()
        return jobapplications