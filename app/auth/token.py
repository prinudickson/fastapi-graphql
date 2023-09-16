import jwt
from datetime import datetime, timedelta

from app.settings.config import TOKEN_EXPIRATION_TIME_MINUTES, SECRET_KEY, ALGORITHM


def generate_token(email):
    expiration_time = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION_TIME_MINUTES)
    payload = {
        "sub": email,
        "exp": expiration_time
    }

    token = jwt.encode(payload, SECRET_KEY, ALGORITHM)
    return token
