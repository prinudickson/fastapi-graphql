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
       return root.jobs

class JobObject(ObjectType):
    id = Int()
    title = String()
    description = String()
    employer_id = Int()
    employer = Field(lambda: EmployerObject)

    @staticmethod
    def resolve_employer(root, info):
        #return next((employer for employer in employers_data if employer["id"] == root["employer_id"]), None)
        return root.employer