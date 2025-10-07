from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from unnoti_corestore.db.connection import SessionLocal
from unnoti_corestore.db.repository import GenericRepository
from sqlalchemy import text
from .user_models import UserCreate, UserResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM sp_get_users()")).fetchall()
    return [{"id": row[0], "username": row[1], "email": row[2]} for row in result]

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    result = db.execute(
        text("SELECT sp_create_user(:username, :email, :password)"),
        {"username": user.username, "email": user.email, "password": user.password}
    )
    user_id = result.scalar()
    if not user_id:
        raise HTTPException(status_code=400, detail="User creation failed")
    return {"id": user_id, "username": user.username, "email": user.email}