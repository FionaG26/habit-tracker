from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from models import User
from schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from database import get_db
from passlib.context import CryptContext
from .auth_utils import (
    create_access_token, 
    create_refresh_token, 
    verify_password, 
    get_current_user, 
    verify_refresh_token, 
    get_password_hash as hash_password
)
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from datetime import timedelta
import os

load_dotenv()

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

STATE_SECRET = os.getenv("STATE_SECRET")

# -----------------------------
# Admin Authorization Dependency
# -----------------------------
def require_admin(current_user: User = Depends(get_current_user)):
    if not hasattr(current_user, "role") or current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    return current_user

# -----------------------------
# OAuth Setup and Endpoints
# -----------------------------
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

@router.get("/google/login", operation_id="google_login", summary="Google OAuth login")
async def google_login(request: Request):
    redirect_uri = f"{os.getenv('BASE_URL')}/auth/google/callback"
    state = os.urandom(16).hex()  # Generate unique state
    request.session["oauth_state"] = state  # Store state in session
    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)

@router.get("/google/callback", operation_id="google_callback", summary="Google OAuth callback")
async def google_callback(request: Request):
    stored_state = request.session.pop("oauth_state", None)
    received_state = request.query_params.get("state")
    if stored_state is None or stored_state != received_state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="State mismatch! Possible CSRF attack.")
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")
    if not user_info or "email" not in user_info:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Google authentication failed")
    access_token = create_access_token(data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": user_info["email"]})
    return RedirectResponse(url=f"{os.getenv('FRONTEND_URL')}/oauth-success?token={access_token}&refresh={refresh_token}")

@router.get("/github/login", operation_id="github_login", summary="GitHub OAuth login")
async def github_login(request: Request):
    redirect_uri = f"{os.getenv('BASE_URL')}/auth/github/callback"
    state = os.urandom(16).hex()
    request.session["oauth_state"] = state
    return await oauth.github.authorize_redirect(request, redirect_uri, state=state)

@router.get("/github/callback", operation_id="github_callback", summary="GitHub OAuth callback")
async def github_callback(request: Request):
    stored_state = request.session.pop("oauth_state", None)
    received_state = request.query_params.get("state")
    if stored_state is None or stored_state != received_state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="State mismatch! Possible CSRF attack.")
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.get("https://api.github.com/user", token=token)
    user_info_json = user_info.json()
    email = user_info_json.get("email")
    if not email:
        emails_response = await oauth.github.get("https://api.github.com/user/emails", token=token)
        emails = emails_response.json()
        email = next((e["email"] for e in emails if e.get("primary", False) and e.get("verified", False)), None)
    if not email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="GitHub email not found")
    access_token = create_access_token(data={"sub": email}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": email})
    return RedirectResponse(url=f"{os.getenv('FRONTEND_URL')}/oauth-success?token={access_token}&refresh={refresh_token}")

# -----------------------------
# JWT Authentication Endpoints
# -----------------------------
@router.post("/register", response_model=TokenResponse, summary="Register a new user and return tokens")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken!")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password, role="user")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    access_token = create_access_token(data={"sub": new_user.username}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": new_user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse, summary="Login user and return JWT tokens")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=60))
    refresh_token = create_refresh_token(data={"sub": db_user.username})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/logout", summary="Client-side logout", operation_id="logout")
def logout():
    return {"message": "Logout successful. Please remove tokens from your client storage."}

@router.post("/refresh", response_model=TokenResponse, summary="Refresh JWT token")
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    payload = verify_refresh_token(refresh_token)
    username = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    db_user = db.query(User).filter(User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    new_access_token = create_access_token(data={"sub": db_user.username}, expires_delta=timedelta(minutes=60))
    return {"access_token": new_access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse, summary="Get current logged-in user")
def get_me(current_user: User = Depends(get_current_user)):
    return UserResponse(username=current_user.username, role=current_user.role)

@router.get("/admin-only", summary="Admin-only test route", operation_id="admin_only")
def admin_only_route(admin: User = Depends(require_admin)):
    return {"message": "Welcome, Admin!"}
