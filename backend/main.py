from fastapi import FastAPI
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

# Ensure session persistence
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SESSION_SECRET_KEY", "supersecretkey"))

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

# Add SessionMiddleware for OAuth sessions
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "your_secure_session_secret"),
    session_cookie="oauth_session",
    same_site="lax"
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(habits_router, prefix="/habits", tags=["Habits"])

# CORS Middleware (Allow frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint for production readiness
@app.get("/health", tags=["Health"], summary="Health Check")
async def health_check():
    return {"status": "ok"}

# Serve frontend if it exists
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")

@app.get("/", include_in_schema=False)
async def serve_vue():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Run npm run build."}
