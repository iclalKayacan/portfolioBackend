from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.projects import Project, ProjectResponse
from app.services.project_service import (
    get_all_projects,
    get_project_by_id,
    create_project as create_project_service,
    update_project as update_project_service,
    delete_project as delete_project_service
)
from app.routers.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/", response_model=list[ProjectResponse])
def list_projects(db: Session = Depends(get_db)):
    return get_all_projects(db)

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int, db: Session = Depends(get_db)):
    return get_project_by_id(db, project_id)

@router.post("/", response_model=ProjectResponse)
def create_project(
    project: Project,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return create_project_service(db, project)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    updated: Project,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    return update_project_service(db, project_id, updated)

@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),  # Only authenticated users can delete
):
    deleted_project = delete_project_service(db, project_id)
    return {"message": "Project deleted", "project_id": project_id}
