from graphene import Mutation, String, Field, Int, Boolean

from app.gql.types import EmployerObject
from app.db.database import SessionLocal
from app.db.models import Employer
from app.auth.auth import get_authenticated_user
            

class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String()

    employer = Field(lambda: EmployerObject)

    authenticated_as = Field(String)

    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        session = SessionLocal()
        user = get_authenticated_user(info.context)
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        
        session.add(employer)
        session.commit()
        session.refresh(employer)
        #session.close()
        return AddEmployer(employer=employer, authenticated_as=user.email)
    

class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contact_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, id, name=None, contact_email=None, industry=None):
        session = SessionLocal()
        em = session.query(Employer).filter(Employer.id==id).first()

        if not em:
            raise Exception("Job not found")
        
        if name is not None:
            em.name = name
        
        if contact_email is not None:
            em.contact_email = contact_email
        
        if industry is not None:
            em.industry = industry

        session.commit()
        session.refresh(em)
        #session.close()
        return UpdateEmployer(employer=em)
    
class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @staticmethod
    def mutate(root, info, id): #title=None, description=None, employer_id=None):
        session = SessionLocal()
        em = session.query(Employer).filter(Employer.id==id).first()

        if not em:
            raise Exception("Job not found")

        session.delete(em)
        session.commit()
        session.close()
        return DeleteEmployer(success=True)
