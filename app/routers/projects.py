from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.projects import Project, ProjectResponse
from app.models.projects import Project as ProjectModel
from app.routers.auth import get_current_username

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return db.query(ProjectModel).all()

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: Project,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username),
):
    new_project = ProjectModel(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    updated: Project,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username),
):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.title = updated.title
    project.description = updated.description
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    username: str = Depends(get_current_username),
):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"message": "Project deleted", "project_id": project_id}
