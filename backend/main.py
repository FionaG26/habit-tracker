from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from routes import auth, habits, users
from database import Base, engine
from dotenv import load_dotenv
import jwt  # PyJWT for token decoding
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Habit Tracker API", version="1.0", redirect_slashes=False)

# OAuth2 for Token Authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# JWT Secret Key (Replace with a secure secret)
SECRET_KEY = os.getenv("JWT_SECRET", "mysecret")
ALGORITHM = "HS256"

# Function to verify JWT token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")

    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# CORS Middleware (Allow frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(habits.router, prefix="/habits", tags=["Habits"])
app.include_router(users.router, prefix="/api", tags=["Users"])

# Protect habits route (User must be logged in)
@app.get("/habits/protected", dependencies=[Depends(get_current_user)])
def get_protected_habits():
    return {"habits": ["Exercise", "Reading", "Meditation"]}


# Define frontend path
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

# Serve frontend files if they exist
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print("⚠️ Frontend directory not found! Run `npm run build`.")

# Serve index.html directly (Fixes Vue routing issues)
@app.get("/", include_in_schema=False)
@app.get("")
async def serve_vue():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Please run `npm run build` and ensure the dist folder is in the backend."}
