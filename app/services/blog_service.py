# app/services/blog_service.py
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional
from datetime import datetime
import re
from app.models.blog import BlogPost
from app.schemas.blog import BlogPostCreate, BlogPostUpdate

def create_slug(title: str) -> str:
    """Başlıktan slug oluşturur"""
    slug = title.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug.strip('-')

def get_all_blog_posts(db: Session, published_only: bool = False) -> List[BlogPost]:
    """Blog yazılarını getirir"""
    query = db.query(BlogPost)
    if published_only:
        query = query.filter(BlogPost.published == True)
    return query.order_by(desc(BlogPost.created_at)).all()

def get_blog_post_by_id(db: Session, post_id: int) -> Optional[BlogPost]:
    """ID ile blog yazısı getirir"""
    return db.query(BlogPost).filter(BlogPost.id == post_id).first()

def create_blog_post(db: Session, post: BlogPostCreate, author_id: int) -> BlogPost:
    """Yeni blog yazısı oluşturur"""
    slug = create_slug(post.title)
    
    db_post = BlogPost(
        title=post.title,
        content=post.content,
        slug=slug,
        excerpt=post.excerpt,
        published=post.published,
        author_id=author_id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_blog_post(db: Session, post_id: int, post_update: BlogPostUpdate) -> Optional[BlogPost]:
    """Blog yazısını günceller"""
    db_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not db_post:
        return None
    
    update_data = post_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_post, field, value)
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_blog_post(db: Session, post_id: int) -> bool:
    """Blog yazısını siler"""
    db_post = db.query(BlogPost).filter(BlogPost.id == post_id).first()
    if not db_post:
        return False
    
    db.delete(db_post)
    db.commit()
    return True
