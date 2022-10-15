from pydantic import BaseSettings


class Settings(BaseSettings):
    db_username:str
    password:int
    db_name:str
    secret_key:str
    algorithm:str
    expire:int
    

    class Config:
        env_file = "app/.env"



settings=Settings()