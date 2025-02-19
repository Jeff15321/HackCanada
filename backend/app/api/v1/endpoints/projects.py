from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List
from app.schemas.project import ProjectResponse
from app.services.projects import ProjectService

router = APIRouter()

@router.get("/")
async def get_all_projects(user_id: str):
    """
    Get all projects for a user
    """
    try:
        return await ProjectService.get_user_projects(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 