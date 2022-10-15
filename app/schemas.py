from unicodedata import name
from pydantic import BaseModel,EmailStr,validator
from typing import Union,Optional
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
    name:str
    email:EmailStr
    
    class Config:
        orm_mode=True


class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    owner: User

    class Config:
        orm_mode=True


class PostsOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode=True

class PostOut(BaseModel):
    Post:Post
    votes:int

    class Config:
        orm_mode=True


class UserVerify(BaseModel):
    email:EmailStr
    password:str

class UserCreate(UserVerify):
    name:str
    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Union[str, None] = None


class Vote(BaseModel):
    post_id:int
    like:int

    @validator('like')
    def validate_like(cls, v):
        if v not in [0,1]:
            raise ValueError('[like] Must be 0 or 1.')
        return v

















