from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from authlib.integrations.starlette_client import OAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Habit Tracker API", version="1.0", redirect_slashes=False)

# Add SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET", "your_secure_session_secret"))

# OAuth setup
oauth = OAuth()

# ✅ Register GitHub OAuth
oauth.register(
    name="github",
    client_id=os.getenv("GITHUB_CLIENT_ID"),
    client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
    authorize_url="https://github.com/login/oauth/authorize",
    access_token_url="https://github.com/login/oauth/access_token",
    userinfo_endpoint="https://api.github.com/user",
    client_kwargs={"scope": "user:email"},
)

# ✅ Register Google OAuth
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
    allow_origins=["http://localhost:5173"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ GitHub OAuth Login
@app.get("/auth/github/login")
async def github_login(request: Request):
    redirect_uri = "http://localhost:8000/auth/github/callback"  # Must match GitHub settings
    return await oauth.github.authorize_redirect(request, redirect_uri)

# ✅ GitHub OAuth Callback
@app.get("/auth/github/callback")
async def github_callback(request: Request):
    token = await oauth.github.authorize_access_token(request)
    user_info = await oauth.github.get("https://api.github.com/user", token=token)

    if not user_info:
        raise HTTPException(status_code=400, detail="GitHub authentication failed")

    user_data = user_info.json()
    return {"user": user_data}

# ✅ Google OAuth Login
@app.get("/auth/google/login")
async def google_login(request: Request):
    redirect_uri = "http://localhost:8000/auth/google/callback"  # Must match Google settings
    return await oauth.google.authorize_redirect(request, redirect_uri)

# ✅ Google OAuth Callback
@app.get("/auth/google/callback")
async def google_callback(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.get("https://www.googleapis.com/oauth2/v2/userinfo", token=token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Google authentication failed")

    user_data = user_info.json()
    return {"user": user_data}

# ✅ Protected Route (Requires Login)
@app.get("/habits/protected")
async def protected_habits():
    return {"habits": ["Exercise", "Reading", "Meditation"]}

# ✅ Serve frontend if exists
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")

# ✅ Serve index.html
@app.get("/", include_in_schema=False)
async def serve_vue():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Run `npm run build`."}
