
from sqlalchemy import Column, Boolean,  ForeignKey, Integer, String
from .database import Base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__='posts'

    id=Column(Integer,primary_key=True,nullable=False)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean, server_default='false',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id=Column(Integer,ForeignKey('users.id',ondelete='CASCADE'))
    owner=relationship("User")

class User(Base): 
    __tablename__='users'

    id=Column(Integer,primary_key=True,nullable=False)
    first_name=Column(String,nullable=True)
    last_name=Column(String,nullable=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))



















