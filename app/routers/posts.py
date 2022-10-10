from fastapi import APIRouter,Depends,Request,Response,HTTPException,status
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from ..auth import get_current_user


router=APIRouter(
    prefix="/posts",
    tags=["posts"]
)

# create a post
@router.post("/",response_model=schemas.Post)
async def create_post(post:schemas.PostCreate,
                     db:Session=Depends(get_db),
                     user:int=Depends(get_current_user)):
    # print(user_id)
    new_post=models.Post(**post.dict(),owner_id=user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# fetch all post
@router.get("/",response_model=List[schemas.Post])
async def get_posts(db:Session=Depends(get_db),
                    user:int=Depends(get_current_user)):
    print('user id->',user.id)
    posts=db.query(models.Post).all()
    from sqlalchemy import inspect
    insp = inspect(models.Post)
    return posts

# fetch a post
@router.get("/{post_id}",response_model=schemas.Post)
async def get_post(post_id:int,db:Session=Depends(get_db),
                    user:int=Depends(get_current_user)):
    query=db.query(models.Post).filter(models.Post.id==post_id)
    if query.first()==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Post with id-{post_id} not found')
    return query.first()

# update a post
@router.put("/{post_id}",response_model=schemas.Post)
async def update_post(post_id:int,post:schemas.PostUpdate , db:Session=Depends(get_db),user:int=Depends(get_current_user)):
    query=db.query(models.Post).filter(models.Post.id==post_id)
    to_update=query.first()
    if to_update==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Post with id-{post_id} does not exist.')
    # print(type(to_update.owner_id))    
    # print(type(user_id.id))    
    if to_update.owner_id != int(user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'You can not update other\'s post.')
    query.update(post.dict(),synchronize_session=False)
    db.commit()
    return query.first()

# delete a post
@router.delete("/{post_id}")
async def delete_post(post_id:int,
                    db:Session=Depends(get_db),
                    user:int=Depends(get_current_user)):
    query=db.query(models.Post).filter(models.Post.id==post_id)
    to_delete=query.first()
    if to_delete==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f'Post with id-{post_id} not found')
    if to_delete.owner_id != int(user.id):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f'You can not delete other\'s post.')
    query.delete()
    db.commit()

    return {"detail":"The post has been removed."}
























