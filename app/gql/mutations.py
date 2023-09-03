from graphene import Mutation, String, Int, Field, ObjectType
from app.gql.types import JobObject
from app.db.database import SessionLocal
from app.db.models import Job

class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        session = SessionLocal()
        session.add(job)
        session.commit()
        session.refresh(job)
        #session.close()
        return AddJob(job=job)
    
class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @staticmethod
    def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        session = SessionLocal()
        u_job = session.query(Job).filter(Job.id==job_id).first()

        if not u_job:
            raise Exception("Job not found")
        
        if title is not None:
            u_job.title = title
        
        if description is not None:
            u_job.description = description
        
        if employer_id is not None:
            u_job.employer_id = employer_id

        session.commit()
        session.refresh(u_job)
        #session.close()
        return UpdateJob(job=u_job)
    
class Mutation(ObjectType):
    add_job  = AddJob.Field()
    update_job = UpdateJob.Field()