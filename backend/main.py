from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from jose import jwt, JWTError
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

# Ensure JWT Secret Key is Loaded
JWT_SECRET = os.getenv("1d088b2ab8611b0132fd6627427ff041b416b5ba86a985345789ce2b7a830d45")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

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
# Function to create JWT token
def create_jwt_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Function to verify JWT token
def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload  # Token is valid
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

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
