from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import Request
from .config import settings

DATABASE_URL = f"postgresql://{settings.db_username}:{settings.password}@localhost/{settings.db_name}"

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

