import string
from random import choices
from graphene import Mutation, String, Int, Field, Boolean
from graphql import GraphQLError
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import jwt
from datetime import datetime, timedelta

from app.gql.types import JobObject
from app.db.database import SessionLocal
from app.db.models import Job, User
from app.settings.config import TOKEN_EXPIRATION_TIME_MINUTES, SECRET_KEY, ALGORITHM

ph = PasswordHasher()

def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token

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
        
        try:
            ph.verify(user.password_hash, password)
        except VerifyMismatchError:
            raise GraphQLError("Invalid Password")
        
        token = generate_token(email)
        
        session.commit()
        session.refresh(user)
        return LoginUser(token = token)