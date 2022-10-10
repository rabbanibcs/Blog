from fastapi import APIRouter,Depends,Request,Response,HTTPException,status
from .. import models,schemas
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from .. import auth
router=APIRouter(
    prefix="/users",
    tags=["users"]
)

# register a user
@router.post("/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User)
async def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    # hash password    
    user.password=auth.hash(user.password)
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# fetch all users
@router.get("/",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.User])
async def get_users(db:Session=Depends(get_db),
                    user_id:int=Depends(auth.get_current_user)):
    return db.query(models.User).all()

# fetch one user
@router.get("/{id}",
    status_code=status.HTTP_302_FOUND,
    response_model=schemas.User)
async def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with id-{id} not found')
    return user


# user login
@router.post("/login",response_model=schemas.Token)
async def login(user_credentials:schemas.UserVerify,
                db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.email==user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"User credentials are not valid.(email not exists)")

    verified=auth.verify_password(user_credentials.password,user.password)
    if verified:
        token=auth.create_access_token(data={"user_id":user.id})
        return {"access_token": token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"User credentials are not valid.(password not matched)")










