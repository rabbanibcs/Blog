
from passlib.context import CryptContext
psw_context=CryptContext(schemes=['bcrypt'])

def hash(password:str):
    return psw_context.hash(password)