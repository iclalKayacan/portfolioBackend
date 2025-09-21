# app/config.py
import os
from dotenv import load_dotenv
from passlib.context import CryptContext

# .env dosyasını yükle
load_dotenv()

# Auth ayarları
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_TO_A_LONG_RANDOM_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Database ayarları
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "portfolio_db")

# Password hashing
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Demo kullanıcılar
USERS = {"demo": {"username": "demo", "hashed": pwd.hash("demo123")}}
