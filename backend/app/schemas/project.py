from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ProjectResponse(BaseModel):
    id: str
    name: str
    created_at: datetime
    is_public: bool
    collaborators: List[str] = [] 