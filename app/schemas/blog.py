# app/schemas/blog.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class BlogPostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    excerpt: Optional[str] = None
    published: bool = False

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1)
    excerpt: Optional[str] = None
    published: Optional[bool] = None

class BlogPostResponse(BlogPostBase):
    id: int
    slug: str
    created_at: datetime
    author_id: int
    
    class Config:
        from_attributes = True
