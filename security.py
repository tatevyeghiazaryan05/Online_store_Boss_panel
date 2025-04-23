from passlib.context import CryptContext
from jose import jwt
import datetime
from fastapi.security.oauth2 import OAuth2PasswordBearer
from fastapi import Depends

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/boss/auth/login")

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
secret_key = "sdfghjkmdxcfvgbhnjkm,l"


def create_access_token(user_data: dict):
    user_data["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    token = jwt.encode(user_data, secret_key, "HS256")
    return token


def verify_access_token(token: str):
    user_data = jwt.decode(token, secret_key, algorithms=["HS256"])
    return user_data


def get_current_user(token=Depends(oauth2_schema)):
    data = verify_access_token(token)
    return data
