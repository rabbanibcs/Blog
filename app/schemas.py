from pydantic import BaseModel,EmailStr

class PostBase(BaseModel):
    title:str
    content:str
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    published:bool

# ctrl + D

class Post(BaseModel):
    title:str
    content:str
    id:int

    class Config:
        orm_mode=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str


class User(BaseModel):
    email:EmailStr
    id:int
    class Config:
        orm_mode=True