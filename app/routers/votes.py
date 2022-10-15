from fastapi import APIRouter, Depends,status,HTTPException
from sqlalchemy.orm import Session
from ..auth import get_current_user
from .. import schemas, models
from ..database import get_db


router=APIRouter(
    prefix="/votes",
    tags=["votes"]
)

# create or remove a vote
@router.post("/",status_code=status.HTTP_201_CREATED)
async def create_vote(vote:schemas.Vote,
                     db:Session=Depends(get_db),
                     user:int=Depends(get_current_user)):
    # print(vote)
    if vote.like==1:
        try:
            new_vote=models.Vote(user_id=user.id,post_id=vote.post_id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return new_vote
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id_{vote.post_id} does not exists.")
    elif vote.like==0:
        query=db.query(models.Vote).filter(models.Vote.user_id==user.id,models.Vote.post_id==vote.post_id)
        if query.first():
            query.delete()
            db.commit()
            return {"detail":"The vote has been removed."}
        else:
            return {"detail":"User not voted on the post."}

    