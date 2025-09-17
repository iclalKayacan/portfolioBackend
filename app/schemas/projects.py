# schemas/projects.py
from pydantic import BaseModel

class Project(BaseModel):
    title: str
    description: str

class ProjectUpdate(Project):
    id: int

class ProjectResponse(BaseModel):
    id: int
    title: str
    description: str
