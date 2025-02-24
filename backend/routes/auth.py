from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from models import User
from schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from database import get_db
from passlib.context import CryptContext
from .auth_utils import create_access_token, verify_password, get_current_user
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from datetime import timedelta, datetime
from security import hash_password, create_access_token, create_refresh_token
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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Google OAuth Route
@router.get("/google/login")
async def google_login(request: Request):
    redirect_uri = f"{os.getenv('BASE_URL')}/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info or "email" not in user_info:
        raise HTTPException(status_code=400, detail="Google authentication failed")

    access_token = create_access_token(data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": user_info["email"]})

    return RedirectResponse(url=f"{os.getenv('FRONTEND_URL')}/oauth-success?token={access_token}&refresh={refresh_token}")

# ✅ GitHub OAuth Route
@router.get("/github/login")
async def github_login(request: Request):
    redirect_uri = f"{os.getenv('BASE_URL')}/auth/github/callback"
    return await oauth.github.authorize_redirect(request, redirect_uri)

@router.get("/github/callback")
async def github_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.get("https://api.github.com/user", token=token)

    user_info_json = user_info.json()
    email = user_info_json.get("email")

    # GitHub might not provide an email directly, so fetch it separately
    if not email:
        emails_response = await oauth.github.get("https://api.github.com/user/emails", token=token)
        emails = emails_response.json()
        email = next((e["email"] for e in emails if e.get("primary", False) and e.get("verified", False)), None)

    if not email:
        raise HTTPException(status_code=400, detail="GitHub email not found")

    access_token = create_access_token(data={"sub": email}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": email})

    return RedirectResponse(url=f"{os.getenv('FRONTEND_URL')}/oauth-success?token={access_token}&refresh={refresh_token}")

# ✅ Register a new user and return tokens
@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the username is already taken
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken!")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create new user (ensure 'role' field exists in the database)
    new_user = User(username=user.username, password=hashed_password, role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate access and refresh tokens
    access_token = create_access_token(data={"sub": new_user.username}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": new_user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ✅ Login user and return JWT tokens
@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # Generate access and refresh tokens
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": db_user.username})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ✅ Refresh Token Endpoint
@router.post("/refresh", response_model=TokenResponse)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_refresh_token(refresh_token)
    username = payload.get("sub")

    if not username:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=60))
    return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# ✅ Get current logged-in user (ensure sensitive data is excluded)
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(username=current_user.username, role=current_user.role)

# ✅ Role-based authorization: Only admins can access certain routes
def require_admin(current_user: User = Depends(get_current_user)):
    if not hasattr(current_user, "role") or current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    return current_user
