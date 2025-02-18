from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import os

router = APIRouter()

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# returns json of all jobs with their tasks
@router.get("/api/jobs")
async def get_jobs():
    try:
        with open(os.path.join(DATA_DIR, 'title_tasks.json'), 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Couldn't load jobs: {str(e)}")