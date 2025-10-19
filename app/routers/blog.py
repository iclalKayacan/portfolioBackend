# app/routers/blog.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.blog import BlogPostCreate, BlogPostUpdate, BlogPostResponse
from app.services.blog_service import (
    get_all_blog_posts, get_blog_post_by_id, create_blog_post, 
    update_blog_post, delete_blog_post
)
from app.routers.auth import get_current_user

router = APIRouter(prefix="/blog", tags=["Blog"])

@router.get("/posts", response_model=List[BlogPostResponse])
def list_blog_posts(published_only: bool = True, db: Session = Depends(get_db)):
    """Blog yazılarını listeler"""
    return get_all_blog_posts(db, published_only)

@router.get("/posts/{post_id}", response_model=BlogPostResponse)
def get_blog_post(post_id: int, db: Session = Depends(get_db)):
    """ID ile blog yazısı getirir"""
    post = get_blog_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Blog yazısı bulunamadı")
    return post

@router.post("/posts", response_model=BlogPostResponse)
def create_blog_post_endpoint(
    post: BlogPostCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Yeni blog yazısı oluşturur"""
    return create_blog_post(db, post, current_user.id)

@router.put("/posts/{post_id}", response_model=BlogPostResponse)
def update_blog_post_endpoint(
    post_id: int,
    post_update: BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Blog yazısını günceller"""
    existing_post = get_blog_post_by_id(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Blog yazısı bulunamadı")
    
    if existing_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu yazıyı düzenleme yetkiniz yok")
    
    updated_post = update_blog_post(db, post_id, post_update)
    return updated_post

@router.delete("/posts/{post_id}")
def delete_blog_post_endpoint(
    post_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Blog yazısını siler"""
    existing_post = get_blog_post_by_id(db, post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Blog yazısı bulunamadı")
    
    if existing_post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Bu yazıyı silme yetkiniz yok")
    
    delete_blog_post(db, post_id)
    return {"message": "Blog yazısı silindi"}
