from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

passwd_context = CryptContext(schemes=["bcrypt"])

def generate_passwd_hash(password: str) -> str:
    hash = passwd_context.hash(password)
    
    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)

def create_access_token(user_data: dict, expiry: timedelta):
    payload = {}
    
    token= jwt.encode(
        payload=payload,
        key=
    )