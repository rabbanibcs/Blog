from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Request
DATABASE_URL = "postgresql://postgres:1924@localhost/blog"

engine= create_engine(DATABASE_URL)

LocalSession=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base=declarative_base()


# Dependency
def get_db(request: Request):
    return request.state.db

