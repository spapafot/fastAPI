from fastapi import status, HTTPException, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session


router = APIRouter(prefix="/votes", tags=['Votes'])

@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post Not Found")

    query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status.HTTP_409_CONFLICT, "Already Voted")
        
        new_vote = models.Vote(user_id = current_user.id, post_id = vote.post_id)
        db.add(new_vote)
        db.commit()

        return {"message": "Added Vote"}
    else:
        if not found_vote:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Vote Not Found")
        
        query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Deleted Vote"}