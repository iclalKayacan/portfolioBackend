# app/services/project_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.projects import Project as ProjectModel
from app.schemas.projects import Project

def get_all_projects(db: Session):
    return db.query(ProjectModel).all()

def get_project_by_id(db: Session, project_id: int):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

def create_project(db: Session, project: Project):
    new_project = ProjectModel(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

def update_project(db: Session, project_id: int, updated: Project):
    project = get_project_by_id(db, project_id)
    project.title = updated.title
    project.description = updated.description
    db.commit()
    db.refresh(project)
    return project

def delete_project(db: Session, project_id: int):
    project = get_project_by_id(db, project_id)
    db.delete(project)
    db.commit()
    return project
