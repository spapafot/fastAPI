from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic.networks import EmailStr
from pydantic.types import conint

class User(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class UserGet(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr

    class Config:
        orm_mode = True
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    owner: UserGet

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

