import string
from random import choices
from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from app.gql.types import JobObject
from app.db.database import SessionLocal
from app.db.models import Job, User

class LoginUser(Mutation):
    class Arguments:
        email = String(required = True)
        password = String(required = True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = SessionLocal()
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("User not found")
        
        if user.password == password:
            token = ''.join(choices(string.ascii_lowercase, k=20))
        else:
            raise GraphQLError("Incorrect Password")
        
        session.commit()
        session.refresh(user)
        return LoginUser(token = token)