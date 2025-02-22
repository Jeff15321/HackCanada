from fastapi import APIRouter
from app.api.v1.endpoints import projects, users, auth, model

api_router = APIRouter()

print("Registering routes...")

api_router.include_router(
    projects.router,
    prefix="/projects",
    tags=["projects"]
)

print("Available project routes:", [
    f"{route.path} [{route.methods}]" 
    for route in projects.router.routes
])

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"]
) 

api_router.include_router(
    model.router,
    prefix="/model",
    tags=["model"]
)
