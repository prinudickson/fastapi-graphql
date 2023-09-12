from graphene import Mutation, String, Field
from app.gql.types import EmployerObject
from app.db.database import SessionLocal
from app.db.models import Employer

class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String()

    employer = Field(lambda: EmployerObject)

    @staticmethod
    def mutate(root, info, name, contact_email, industry):
        employer = Employer(name=name, contact_email=contact_email, industry=industry)
        session = SessionLocal()
        session.add(employer)
        session.commit()
        session.refresh(employer)
        #session.close()
        return AddEmployer(employer=employer)