from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.sql.expression import outerjoin
from sqlalchemy.sql.functions import count
from ..database import get_db
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get("/", response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),  limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    results = db.query(models.Post, count(models.Vote.post_id).label("votes")) \
                .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
                .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(user_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    
    post = db.query(models.Post, count(models.Vote.post_id).label("votes")) \
             .join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True) \
             .group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post Does Not Exist") 
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post Does Not Exist")
    if post.user_id != current_user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Not Authorized")
    
    db.delete(post)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Post Does Not Exist")
    if updated_post.user_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Not Authorized")
    
    post_query.update(post.dict())  
    db.commit()

    return post_query.first()
