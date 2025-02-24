from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from database import get_db
from passlib.context import CryptContext
from .auth_utils import create_access_token, verify_password, get_current_user
from authlib.integrations.starlette_client import OAuth
from starlette.responses import RedirectResponse
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

router = APIRouter()

# Initialize OAuth
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params={"scope": "openid email profile"},
    access_token_url="https://oauth2.googleapis.com/token",
    access_token_params=None,
    client_kwargs={"scope": "openid email profile"},
)

oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    client_kwargs={"scope": "user:email"},
)

# Google OAuth Route
@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = f"{os.getenv('BASE_URL')}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    
    if not user_info:
        raise HTTPException(status_code=400, detail="Google authentication failed")
    
    access_token = create_access_token(data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=60))
    return RedirectResponse(url=f"{os.getenv('FRONTEND_URL')}/oauth-success?token={access_token}")

# GitHub OAuth Route
@router.get("/github/login")
async def github_login(request: Request):
    redirect_uri = f"{os.getenv('BASE_URL')}/auth/github/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)

@router.get("/github/callback")
async def github_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.get("https://api.github.com/user", token=token)
    
    if not user_info:
        raise HTTPException(status_code=400, detail="GitHub authentication failed")
    
    access_token = create_access_token(data={"sub": user_info.json()["email"]}, expires_delta=timedelta(minutes=60))
    return RedirectResponse(url=f"{os.getenv('FRONTEND_URL')}/oauth-success?token={access_token}")

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
