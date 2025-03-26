from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from typing import Optional, List

# Response Models

# Users
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class User(UserBase):
    password: str
    id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

# Auth
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# Posts
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostWithVotes(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    votes: int
    owner: UserOut 

    class Config:
        from_attributes = True

class PostList(BaseModel):
    posts: List[PostWithVotes]

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    model_config = ConfigDict(from_attributes=True)

# Votes
class Vote(BaseModel):
    post_id: int
    dir: int = Field(ge=0, le=1)

