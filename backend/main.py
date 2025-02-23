from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, habits
from database import Base, engine
from routes import users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Initialize FastAPI app
app = FastAPI(title="Habit Tracker API", version="1.0")

# Enable CORS (for Svelte frontend to communicate with FastAPI)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with deployed frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables (Ensure tables exist on startup)
Base.metadata.create_all(bind=engine)

# Include authentication and habit management routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(habits.router, prefix="/habits", tags=["Habits"])
app.include_router(users.router, prefix="/api", tags=["Users"])

# Serve Vue frontend
app.mount("/frontend", StaticFiles(directory="frontend", html=True), name="frontend")

@app.get("/")
async def serve_vue():
    return FileResponse("frontend/index.html")
