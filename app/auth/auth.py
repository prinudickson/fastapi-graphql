import jwt
from functools import wraps
from graphql import GraphQLError
from datetime import datetime, timezone
from app.db.models import User
from app.db.database import SessionLocal
from app.settings.config import SECRET_KEY, ALGORITHM



def get_authenticated_user(context):
    request_object = context.get('request')
    auth_header = request_object.headers.get('Authorization')

    token_list = auth_header.split(" ")

    if auth_header and token_list[0] == "Bearer" and len(token_list) == 2:

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            if datetime.now(timezone.utc) > datetime.fromtimestamp(payload['exp'], tz=timezone.utc):
                raise GraphQLError("Token has expired")
            
            session = SessionLocal()

            user = session.query(User).filter(User.email ==payload.get('sub')).first()

            if not user:
                raise GraphQLError("Could not authenticate user!")
            
            return user
        except jwt.exceptions.PyJWTError:
            raise GraphQLError("Invalid jwt token")
        except Exception as e:
            raise GraphQLError("Invalid jwt token error but not a PyJWTError")
        
    else:
        raise GraphQLError("Missing Authentication Token or Unsupported Authentication token format")
    

def auth_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        get_authenticated_user(info.context)
        return func(*args, **kwargs)
    return wrapper



def auth_user_sameas(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        uid = kwargs.get('user_id')

        if user.id != uid:
            raise GraphQLError("Not Authorised: You cannot apply to jobs for another person!!")
        else: 
            pass
        return func(*args, **kwargs)
    return wrapper
