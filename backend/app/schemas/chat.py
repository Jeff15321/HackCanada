from pydantic import BaseModel
from typing import Dict, Any, Optional

class ChatMessage(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None 