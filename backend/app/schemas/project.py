from pydantic import BaseModel
from typing import List
from datetime import datetime

class ProjectCreate(BaseModel):
    user_id: str
    project_name: str
    collaborators: List[str]
    is_public: bool

class ProjectResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    is_public: bool
    collaborators: List[str]
    user_id: str

    class Config:
        from_attributes = True 