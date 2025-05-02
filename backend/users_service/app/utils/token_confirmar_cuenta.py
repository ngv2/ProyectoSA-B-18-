import uuid
from datetime import datetime, timedelta
import os

def generate_confirmation_token():
    token = str(uuid.uuid4())
    expires = datetime.utcnow() + timedelta(minutes=int(os.getenv("TOKEN_EXP_MINUTES")))
    return token, expires

def verify_token_expiration(expiration_time):
    return datetime.utcnow() < expiration_time