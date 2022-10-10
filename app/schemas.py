from pydantic import BaseModel,EmailStr
from typing import Union
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published:bool

# ctrl + D

class User(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True


class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    owner_id:int
    owner: User


    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserVerify(UserCreate):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Union[str, None] = None



















