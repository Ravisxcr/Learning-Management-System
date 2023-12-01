from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from typing import Annotated, Union
import jwt
import re
from datetime import timedelta, datetime

from schemas import *
from database import *
from main import oth2_scheme

SECRET_KEY  =  "24bee0493c01b636e8a0fefb5beb37e7420eee7b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_cxt = CryptContext(schemes=["bcrypt"],  deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_cxt.verify(plain_password, hashed_password)

def get_hash_password(password: str):
    return pwd_cxt.hash(password)


def create_access_token(data: dict,role,  expires_delta: Union[timedelta, None] = None):
    # to_encode = data.copy()
    try:
        to_encode ={
            "username": data.username,
            "password": data.password,
            "role": role,
            "exp" : datetime.utcnow()+timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
            }
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as ex:
        print(str(ex))
        raise ex
    




async def very_token(token: str):
    '''verify token from login'''
    try:
        payload = jwt.decode(token, SECRET_KEY,
                             algorithms=["HS256"])
        user = User.get(sid=payload.get("username"))

    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

def check_active(token: str = Depends(oth2_scheme)):
    print("abc")
    payload = very_token(token)
    active = payload.get("is_active")
    print("3----------")
    if not active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please activate your Account first",
            headers={"WWW-Authenticate": "Bearer"},
        )
    else:
        return payload
    

if __name__ == "__main__":
    to_encode ={
            "username": "ravi",
            "password": "nopass",
            "exp" : datetime.utcnow()+timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
            }
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(encoded_jwt)

    payload = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGORITHM])
    print(payload)
