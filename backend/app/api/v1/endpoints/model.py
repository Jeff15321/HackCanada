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

        result = await ModelService.create_model(
            userId=userId,
            imageUrl=imageUrl,
            model_name=model_name,
            model_description=model_description,
            model_image_url=model_image_url,
            model_image_file=model_image_file,
            model_attributes=model_attributes_dict
        )

        # Return the full response including all the analysis data
        return ModelResponse(
            success=result["success"],
            message=result["message"],
            api1_data=result.get("api1_data"),
            api2_data=result.get("api2_data"),
            gpt_analysis=result.get("gpt_analysis"),
            combined_score=result.get("combined_score")
        )
    except Exception as e:
        print(f"Error creating model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all/")
async def get_all_models():
    """
    Get all models
    """
    try:
        models = await ModelService.get_all_models()
        return models
    except Exception as e:
        print(f"Error in get_all_models endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# @router.get("/all/")
# async def get_all_projects(user_id: str):
#     """
#     Get all projects for a user
#     """
#     print(f"Received request for user_id: {user_id}")
#     try:
#         print("Fetching projects from service")
#         projects = await ProjectService.get_user_projects(user_id)
#         print(f"Found {len(projects)} projects")
#         return projects
#     except Exception as e:
#         print(f"Error in get_all_projects: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @router.delete("/delete/")
# async def delete_project(project_id: str):
#     """
#     Delete a project
#     """
#     try:
#         print(f"Attempting to delete project: {project_id}")
#         result = await ProjectService.delete_project(project_id)
#         print(f"Delete result: {result}")
#         return result
#     except Exception as e:
#         print(f"Error deleting project: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @router.post("/new/", response_model=ProjectResponse)
# async def new_project(project: ProjectCreate):
#     """
#     Create a new project
#     """
#     try:
#         return await ProjectService.create_project(
#             project.user_id,
#             project.project_name,
#             project.collaborators,
#             project.is_public
#         )
#     except Exception as e:
#         print(f"Error creating project: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# @router.get("/get_one/")
# async def get_chat_history(project_id: str):
#     """
#     Get the chat history for a project
#     """
#     try:
#         result = await ProjectService.get_one(project_id)
#         return result
#     except Exception as e:
#         print(f"Error in get_chat_history endpoint: {str(e)}")
#         raise HTTPException(
#             status_code=500, 
#             detail=f"Failed to get chat history: {str(e)}"
#         )

@router.post("/{model_id}/update-owner")
async def update_owner(model_id: str, new_owner_id: str = Form(...)):
    """
    Update the owner of a model
    """
    try:
        result = await ModelService.update_owner(model_id, new_owner_id)
        return result
    except Exception as e:
        print(f"Error in update_owner endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pipeline/run")
async def run_pipeline(data: dict):
    """
    Run the pipeline with test data
    """
    try:
        result = await ModelService.run_pipeline(data)
        return result
    except Exception as e:
        print(f"Error in run_pipeline endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))