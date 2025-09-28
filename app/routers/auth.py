from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user, get_user_by_username
from app.services.auth_service import (
    create_access_token,
    create_refresh_token,
    authenticate_user,
    verify_token,
)

router = APIRouter(prefix="/auth", tags=["Auth"])

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Authentication dependency
async def get_current_username(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> str:
    payload = verify_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return username

# ✅ Kullanıcı kaydı
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

# ✅ Kullanıcı girişi
@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ✅ Refresh token ile yeni access token alma
@router.post("/refresh")
def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    new_access = create_access_token({"sub": payload["sub"]})
    return {"access_token": new_access, "token_type": "bearer"}

# ✅ Mevcut kullanıcı bilgileri
@router.get("/me", response_model=UserResponse)
def me(username: str = Depends(get_current_username), db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    return user
