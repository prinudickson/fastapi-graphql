from functools import wraps
from graphql import GraphQLError

from app.auth.auth import get_authenticated_user


def admin_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        info = args[1]
        user = get_authenticated_user(info.context)
        if user.role != 'admin':
            raise GraphQLError("Admin Task: You are not authorised to perform this!")
        else: 
            pass
        return func(*args, **kwargs)
    return wrapper


