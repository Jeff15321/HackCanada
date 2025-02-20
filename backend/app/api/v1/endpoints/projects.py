from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List
from app.schemas.project import ProjectResponse, ProjectCreate
from app.services.projects import ProjectService

router = APIRouter()

@router.get("/all/")
async def get_all_projects(user_id: str):
    """
    Get all projects for a user
    """
    print(f"Received request for user_id: {user_id}")
    try:
        print("Fetching projects from service")
        projects = await ProjectService.get_user_projects(user_id)
        print(f"Found {len(projects)} projects")
        return projects
    except Exception as e:
        print(f"Error in get_all_projects: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/")
async def delete_project(project_id: str):
    """
    Delete a project
    """
    try:
        print(f"Attempting to delete project: {project_id}")
        result = await ProjectService.delete_project(project_id)
        print(f"Delete result: {result}")
        return result
    except Exception as e:
        print(f"Error deleting project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/new/", response_model=ProjectResponse)
async def new_project(project: ProjectCreate):
    """
    Create a new project
    """
    try:
        return await ProjectService.create_project(
            project.user_id,
            project.project_name,
            project.collaborators,
            project.is_public
        )
    except Exception as e:
        print(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

