from graphene import Schema, ObjectType, List, Field, String, Int, Float

from app.db.data import employers_data, jobs_data
from app.db.database import SessionLocal
from app.db.models import Employer, Job

class EmployerObject(ObjectType):
    id = Int()
    name = String()
    contact_email = String()
    industry = String()
    jobs = List(lambda: JobObject)

    @staticmethod
    def resolve_jobs(root, info):
       return root.job

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)
    jobapplications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_employer(root, info):
        #return next((employer for employer in employers_data if employer["id"] == root["employer_id"]), None)
        return root.employer
    
    @staticmethod
    def resolve_jobapplications(root, info):
        return root.job_application
    
class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    role = String()
    jobapplications = List(lambda: JobApplicationObject)

    @staticmethod
    def resolve_jobapplications(root, info):
        return root.job_application

class JobApplicationObject(ObjectType):
    id = Int()
    user_id = Int()
    job_id = Int()
    user = Field(lambda: UserObject)
    job = Field(lambda: JobObject)

    @staticmethod
    def resolve_user(root, info):
        return root.user
    
    @staticmethod
    def resolve_job(root, info):
        return root.job