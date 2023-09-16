from argon2 import PasswordHasher
from graphql import GraphQLError
from argon2.exceptions import VerifyMismatchError

def hash_password(pwd):
    ph = PasswordHasher()
    y = ph.hash(pwd)
    return y

def decrypt_password(pwd_hash, pwd):
    ph = PasswordHasher()
    try:
        ph.verify(pwd_hash, pwd)
    except VerifyMismatchError:
        raise GraphQLError("Invalid Password")
    return None