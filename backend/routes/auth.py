from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from database import get_db
from passlib.context import CryptContext
from .auth_utils import create_access_token, verify_password, get_current_user
from datetime import timedelta

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Register a new user and return a token
@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # ✅ Ensure token expiration is consistent
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=60))

    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Login user and return JWT token
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Ensure login tokens have the same expiration time
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=60))

    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Get current logged-in user (return only necessary data)
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

# ✅ Role-based authorization: Only admins can access certain routes
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user
