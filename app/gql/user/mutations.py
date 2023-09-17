

from graphene import Mutation, String, Field, Int, Boolean
from graphql import GraphQLError

from app.gql.types import UserObject, JobApplicationObject
from app.db.database import SessionLocal
from app.db.models import User, JobApplication
from app.auth.token import generate_token
from app.auth.hash import decrypt_password, hash_password
from app.auth.auth import get_authenticated_user, auth_user, auth_user_sameas
from app.auth.admin import admin_user


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
        
        decrypt_password(user.password_hash, password)
        
        token = generate_token(email)

        session.commit()
        session.refresh(user)
        return LoginUser(token = token)
    

class AddUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String()
        role = String()

    user = Field(lambda: UserObject)

    authenticated_as = Field(String)

    @admin_user
    @staticmethod
    def mutate(root, info, username, password, email, role):
        loginuser = get_authenticated_user(info.context)
        # if role =="admin":
        #     if loginuser.role =="admin":
        #         pass
        #     else:
        #         raise GraphQLError("Only admins are allowed to register admins!")

        session = SessionLocal()
        password_hash = hash_password(password)

        check_email = session.query(User).filter(User.email==email).first()
        if not check_email:
            pass 
        else:
            raise GraphQLError("Email already exists")
        
        user = User(username=username, password_hash=password_hash, email=email, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)

        return AddUser(user=user, authenticated_as=loginuser.email)
    

class ApplyJob(Mutation):
    class Arguments:
        user_id = Int(required=True)
        job_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject) 

    @auth_user_sameas
    @staticmethod
    def mutate(root, info, user_id, job_id):
        session = SessionLocal()

        job_application_check = session.query(JobApplication).filter(
            JobApplication.user_id == user_id,
            JobApplication.job_id == job_id
            ).first()

        print
        if job_application_check:
            raise GraphQLError("User has already applied for job!")
        
        job_application = JobApplication(user_id=user_id, job_id=job_id)
        session.add(job_application)
        session.commit()
        session.refresh(job_application)

        return ApplyJob(job_application=job_application)
    
