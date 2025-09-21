# app/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# .env dosyasını yükle
load_dotenv()

# MySQL bağlantı ayarları
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "portfolio_db")

# MySQL bağlantı URL'i
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# engine oluştur
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # SQL sorgularını konsola yazdır (geliştirme için)
    pool_pre_ping=True,  # Bağlantı sağlığını kontrol et
    pool_recycle=300,  # Bağlantıları 5 dakikada bir yenile
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
