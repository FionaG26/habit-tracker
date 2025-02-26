from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from authlib.integrations.starlette_client import OAuth
import os
import logging
from dotenv import load_dotenv
from routes.auth import router as auth_router
from routes.users import router as users_router
from routes.habits import router as habits_router

# Load environment variables
load_dotenv()

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize FastAPI app with metadata for better docs
app = FastAPI(
    title="Habit Tracker API",
    version="1.0",
    description="A FastAPI backend for tracking habits with OAuth and JWT authentication.",
    redirect_slashes=False
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(habits_router, prefix="/habits", tags=["Habits"])

# Add SessionMiddleware for OAuth sessions
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "your_secure_session_secret"))

# OAuth setup
oauth = OAuth()

oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    userinfo_endpoint="https://api.github.com/user",
    client_kwargs={"scope": "user:email"},
)

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    access_token_url="https://oauth2.googleapis.com/token",
    userinfo_endpoint="https://www.googleapis.com/oauth2/v2/userinfo",
    client_kwargs={"scope": "openid email profile"},
)

# CORS Middleware (Allow frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OAuth Endpoints with explicit operation_id and logging

@app.get("/auth/github/login", operation_id="github_login", tags=["Authentication"])
async def github_login(request: Request):
    """
    Redirect to GitHub for OAuth authentication.
    """
    redirect_uri = os.getenv("GITHUB_REDIRECT_URI", "http://localhost:8000/auth/github/callback")
    logger.info("Redirecting to GitHub OAuth endpoint.")
    return await oauth.github.authorize_redirect(request, redirect_uri)

@app.get("/auth/github/callback", operation_id="github_callback", tags=["Authentication"])
async def github_callback(request: Request):
    """
    Handle GitHub OAuth callback.
    """
    try:
        token = await oauth.github.authorize_access_token(request)
        user_info = await oauth.github.get("https://api.github.com/user", token=token)
        if not user_info:
            raise HTTPException(status_code=400, detail="GitHub authentication failed")
        logger.info("GitHub OAuth successful.")
        return {"user": user_info.json()}
    except Exception as e:
        logger.error(f"GitHub OAuth error: {e}")
        raise HTTPException(status_code=400, detail="GitHub authentication error")

@app.get("/auth/google/login", operation_id="google_login", tags=["Authentication"])
async def google_login(request: Request):
    """
    Redirect to Google for OAuth authentication.
    """
    redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "http://localhost:8000/auth/google/callback")
    logger.info("Redirecting to Google OAuth endpoint.")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/google/callback", operation_id="google_callback", tags=["Authentication"])
async def google_callback(request: Request):
    """
    Handle Google OAuth callback.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.get("https://www.googleapis.com/oauth2/v2/userinfo", token=token)
        if not user_info:
            raise HTTPException(status_code=400, detail="Google authentication failed")
        logger.info("Google OAuth successful.")
        return {"user": user_info.json()}
    except Exception as e:
        logger.error(f"Google OAuth error: {e}")
        raise HTTPException(status_code=400, detail="Google authentication error")

# Protected endpoint example
@app.get("/habits/protected", tags=["Habits"])
async def protected_habits():
    return {"habits": ["Exercise", "Reading", "Meditation"]}

# Health check endpoint for production readiness
@app.get("/health", tags=["Health"], summary="Health Check")
async def health_check():
    return {"status": "ok"}

# Serve frontend if exists
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/", include_in_schema=False)
async def serve_vue():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Run `npm run build`."}
