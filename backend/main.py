from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, habits, users
from database import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

# Initialize FastAPI app
app = FastAPI(title="Habit Tracker API", version="1.0")

# Enable CORS (allow frontend to communicate with backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Update with deployed frontend URL if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Include authentication and habit management routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(habits.router, prefix="/habits", tags=["Habits"])
app.include_router(users.router, prefix="/api", tags=["Users"])

# Define frontend directory path
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")

# Serve Vue frontend (Ensure `npm run build` is executed before running FastAPI)
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print("⚠️ Frontend directory not found! Run `npm run build` in the Vue project.")

@app.get("/")
async def serve_vue():
    index_path = os.path.join(frontend_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "Frontend build not found. Please run `npm run build` and place the dist folder in the backend directory."}

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
