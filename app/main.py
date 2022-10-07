from .database import LocalSession,engine,get_db
from fastapi import FastAPI,Depends,Request,Response,HTTPException,status
from sqlalchemy.orm import Session
# from sqlalchemy import 
from . import models,schemas,utils
from typing import List

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = LocalSession()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response








@app.get("/posts",response_model=List[schemas.Post])
async def get_posts(db:Session=Depends(get_db)):
    posts=db.query(models.Post).all()
    from sqlalchemy import inspect
    insp = inspect(models.Post)
    # print(list(insp.columns))
    # print(insp.all_orm_descriptors.keys())
    return posts


@app.get("/post/{post_id}",response_model=schemas.Post)
async def get_post(post_id:int,db:Session=Depends(get_db)):
    query=db.query(models.Post).filter(models.Post.id==post_id)
    if query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Post with id-{post_id} not found')
    return query.first()

@app.post("/post",response_model=schemas.Post)
async def create_post(post:schemas.PostCreate, db:Session=Depends(get_db)):
    # new_post=models.Post(title=post.title,content=post.content)
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



@app.put("/post/{post_id}",response_model=schemas.Post)
async def update_post(post_id:int,post:schemas.PostUpdate ,db:Session=Depends(get_db)):
    query=db.query(models.Post).filter(models.Post.id==post_id)
    # post_=post_query.first()
    print(query)
    query.update(post.dict(),synchronize_session=False)
    db.commit()
    return query.first()


@app.delete("/post/{post_id}")
async def delete_post(post_id:int,db:Session=Depends(get_db)):
    query=db.query(models.Post).filter(models.Post.id==post_id)
    if query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Post with id-{post_id} not found')
    query.delete()
    db.commit()

    return {"detail":"The post has been removed."}


@app.post("/user",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.User)
async def create_user(user:schemas.UserCreate, db:Session=Depends(get_db)):
    # hash password    
    user.password=utils.hash(user.password)
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users",
    status_code=status.HTTP_200_OK,
    response_model=List[schemas.User])
async def get_posts(db:Session=Depends(get_db)):
    return db.query(models.User).all()

@app.get("/user/{id}",
    status_code=status.HTTP_302_FOUND,
    response_model=schemas.User)
async def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if user==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'User with id-{id} not found')
    return user