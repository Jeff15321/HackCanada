from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.model import ModelResponse
from app.services.model import ModelService
import json

router = APIRouter()

@router.post("/new/", response_model=ModelResponse)
async def new_model(
    userId: str = Form(...),
    imageUrl: str = Form(...),
    model_name: str = Form(''),
    model_description: str = Form(''),
    model_image_url: str = Form(''),
    model_image_file: UploadFile = File(None),
    model_attributes: str = Form('{}')
):
    """
    Create a new model
    """
    try:
        # Convert model_attributes from JSON string to dict
        model_attributes_dict = json.loads(model_attributes)
        
        # Log received data
        print(f"Received data: userId={userId}, imageUrl={imageUrl}, model_name={model_name}")
        if model_image_file:
            print(f"Received image file: {model_image_file.filename}")

        return await ModelService.create_model(
            userId=userId,
            imageUrl=imageUrl,
            model_name=model_name,
            model_description=model_description,
            model_image_url=model_image_url,
            model_image_file=model_image_file,
            model_attributes=model_attributes_dict
        )
    except Exception as e:
        print(f"Error creating model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
