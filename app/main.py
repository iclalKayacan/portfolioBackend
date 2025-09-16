# app/main.py
from fastapi import FastAPI
from app.routers import about, projects, auth
from app.database import Base, engine
from app.models import projects as project_models

# tabloları oluştur (eğer yoksa)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastAPI Demo")

# Include routers
app.include_router(about.router)
app.include_router(projects.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


# uvicorn main:app --reload
