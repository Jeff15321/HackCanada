from pydantic import BaseModel
from typing import Dict, Any, Optional

class ModelCreate(BaseModel):
    userId: str
    imageUrl: str
    model_name: str = ''
    model_description: str = ''
    model_image_url: str = ''
    model_image_file: Optional[str] = None
    model_attributes: Dict[str, Any] = {}

class ModelResponse(BaseModel):
    success: bool = True
    message: str = "Model created successfully"
    api1_data: Optional[Dict[str, Any]] = None
    api2_data: Optional[Dict[str, Any]] = None
    gpt_analysis: Optional[str] = None
    combined_score: Optional[float] = None
