from jose import JWTError, jwt,ExpiredSignatureError
from datetime import datetime, timedelta
from typing import Union
from fastapi import HTTPException,Depends,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from . import schemas, models,utils
from passlib.context import CryptContext
from .config import settings
# settings=Settings()
psw_context=CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/login")


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.expire


def hash(password:str):
    return psw_context.hash(password)

def verify_password(password:str,hashed_pwd):
    return psw_context.verify(password,hashed_pwd)

def get_user(user_credentials,db):
    user=db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"User credentials are not valid.")
    return user

def create_access_token(data: dict):
    print(data)
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token:str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception
    return token_data

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_access_token(token)












































