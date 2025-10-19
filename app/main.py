# app/main.py
import logging
from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.routers import about, projects, auth, blog
from app.database import Base, engine
from app.middleware import setup_middleware

# Logging ayarla
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="FastAPI Demo",
    description="FastAPI ile geliştirilmiş demo proje",
    version="1.0.0"
)

# Rate limiting setup
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware'leri ekle
setup_middleware(app)

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 FastAPI Demo uygulaması başlatılıyor...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("📊 Veritabanı tabloları oluşturuldu")
    except Exception as exc:
        logger.exception("❌ Veritabanı tabloları oluşturulurken hata oluştu: %s", exc)
    logger.info("✅ Uygulama hazır!")

# Include routers
app.include_router(about.router)
app.include_router(projects.router)
app.include_router(auth.router)
app.include_router(blog.router)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running!"}


# uvicorn app.main:app --reload
