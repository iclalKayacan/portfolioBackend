# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite bağlantısı (dosya tabanlı)
SQLALCHEMY_DATABASE_URL = "sqlite:///./portfolio.db"

# engine oluştur
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class (model tanımları buradan türeyecek)
Base = declarative_base()

# Dependency: FastAPI endpointlerinde kullanacağız
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
