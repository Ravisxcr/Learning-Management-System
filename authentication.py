from fastapi import HTTPException, status, Depends
from typing import Annotated, Union
from jose import JWTError, jwt
from datetime import timedelta, datetime
from schemas import *
from database import *


SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, role,  expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    try:
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        to_encode.update({"role" : role})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as ex:
        print(str(ex))
        raise ex
    




async def very_token(token: str):
    '''verify token from login'''
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=["HS256"])
        user = User.get(sid=payload.get("username"))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return user

    