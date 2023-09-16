import jwt
from graphql import GraphQLError
from datetime import datetime, timezone
from app.db.models import User
from app.db.database import SessionLocal
from app.settings.config import SECRET_KEY, ALGORITHM



def get_authenticated_user(context):
    request_object = context.get('request')
    print(request_object)
    auth_header = request_object.headers.get('Authorization')
    print(auth_header)

    if auth_header:
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
        except jwt.exceptions.InvalidSignatureError:
            raise GraphQLError("Invalid jwt token")
        
    else:
        raise GraphQLError("Missing Authentication Token")