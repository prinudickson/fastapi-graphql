from graphene import ObjectType, List

from .types import JobObject, EmployerObject

from db.data import jobs_data, employers_data



class Query(ObjectType):
    jobs = List(JobObject)
    employers = List(EmployerObject)

    @staticmethod
    def resolve_jobs(self, info):
        return jobs_data
    
    @staticmethod
    def resolve_employers(self, info):
        return employers_data 
