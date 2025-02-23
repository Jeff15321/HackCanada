from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import os
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import connect_to_mongo, close_mongo_connection
from app.routers import pipeline

# Create uploads directory if it doesn't exist
os.makedirs("uploads/images", exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description=settings.PROJECT_DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
)

print(f"API prefix is: {settings.API_V1_STR}")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database events
app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# Include routers
app.include_router(api_router, prefix=settings.API_V1_STR)

# Mount static files directory
app.mount("/uploads", StaticFiles(directory="uploads", html=True), name="uploads")

app.include_router(pipeline.router, prefix="/v1/pipeline", tags=["pipeline"])

# Serve index.html for root path
@app.get("/")
async def read_root():
    return {"message": "API is running"}

# Print all registered routes
print("\nRegistered routes:")
for route in app.routes:
    if hasattr(route, "methods"):  # Only print API routes, not static file routes
        print(f"{route.path} [{route.methods}]") 

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
