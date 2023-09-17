import jwt
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

TOKEN_EXPIRATION_TIME_MINUTES = int(os.getenv('TOKEN_EXPIRATION_TIME_MINUTES'))
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token
