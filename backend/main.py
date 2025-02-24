from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from routes import auth, habits, users
from database import Base, engine
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app without automatic redirects
app = FastAPI(title="Habit Tracker API", version="1.0", redirect_slashes=False)

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes and handle both /route and /route/ without redirects
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(habits.router, prefix="/habits", tags=["Habits"])
app.include_router(users.router, prefix="/api", tags=["Users"])

# Define frontend path
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

# Serve frontend files if they exist
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print("⚠️ Frontend directory not found! Run `npm run build`.")

# Serve index.html directly without redirect issues
@app.get("/", include_in_schema=False)
@app.get("")
async def serve_vue():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Please run `npm run build` and ensure the dist folder is in the backend."}
