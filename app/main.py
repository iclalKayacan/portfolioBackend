# app/main.py
import logging
from fastapi import FastAPI
from app.routers import about, projects, auth
from app.database import Base, engine
from app.models import projects as project_models
from app.middleware import setup_middleware

# Logging ayarla
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# tabloları oluştur (eğer yoksa)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FastAPI Demo",
    description="FastAPI ile geliştirilmiş demo proje",
    version="1.0.0"
)

# Middleware'leri ekle
setup_middleware(app)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI Demo uygulaması başlatılıyor...")
    logger.info("📊 Veritabanı tabloları oluşturuldu")
    logger.info("✅ Uygulama hazır!")

# Include routers
app.include_router(about.router)
app.include_router(projects.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


# uvicorn main:app --reload
