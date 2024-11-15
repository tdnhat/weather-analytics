from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.province import Province
from src.context.database import get_db

router = APIRouter(
    prefix="/provinces",
    tags=["provinces"]
)

@router.get("/provinces")
def get_provinces(db: Session = Depends(get_db)):
    provinces = db.query(Province).all()
    return provinces
