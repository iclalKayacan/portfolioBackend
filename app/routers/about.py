from fastapi import APIRouter

router = APIRouter(prefix="/about", tags=["About"])

@router.get("/")
def get_about():
    return {
        "name": "İclal",
        "location": "Atakum Samsun",
        "bio": "software engineer, FastAPI öğreniyor!"
    }
