# app/routers/auth.py
from datetime import datetime, timedelta, timezone
import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

# --- Basit ayarlar ---
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_ME_TO_A_LONG_RANDOM_SECRET")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Demo kullanıcı: username=demo, password=demo123
USERS = {"demo": {"username": "demo", "hashed": pwd.hash("demo123")}}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# --- Schemas (isteğe bağlı ama temiz) ---
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class MeResponse(BaseModel):
    username: str

# --- Helpers ---
def create_access_token(sub: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": sub, "exp": exp}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_username(token: str) -> str:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    if not username:
        raise JWTError("no sub")
    return username

async def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    try:
        return decode_username(token)
    except ExpiredSignatureError:
        # Önemli: OAuth2 için bu header’ı ekle
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# --- Routes ---
@router.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends()):
    user = USERS.get(form.username)
    if not user or not pwd.verify(form.password, user["hashed"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(sub=user["username"])
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=MeResponse)
def me(username: str = Depends(get_current_username)):
    return {"username": username}
