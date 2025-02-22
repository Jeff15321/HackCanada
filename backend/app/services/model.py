from typing import Dict, Any, Optional
from fastapi import UploadFile
import random
import asyncio


class ModelService:
    @staticmethod
    async def create_model(
        userId: str,
        imageUrl: str,
        model_name: str = '',
        model_description: str = '',
        model_image_url: str = '',
        model_image_file: Optional[UploadFile] = None,
        model_attributes: Dict[str, Any] = {}
    ):
        try:
            print(f"Received model data: userId={userId}, imageUrl={imageUrl}")

            # Placeholder for two API calls
            async def api_call_1():
                # Simulate API delay
                await asyncio.sleep(1)
                return {
                    "api1_result": "success",
                    "score": random.randint(0, 100)
                }

            async def api_call_2():
                # Simulate API delay
                await asyncio.sleep(2)
                return {
                    "api2_result": "success",
                    "confidence": random.randint(0, 100)
                }

            # Call both APIs concurrently
            api1_result, api2_result = await asyncio.gather(
                api_call_1(),
                api_call_2()
            )

            print("API 1 Result:", api1_result)
            print("API 2 Result:", api2_result)

            # Process file if available
            if model_image_file:
                contents = await model_image_file.read()
                print(f"Image file size: {len(contents)} bytes")
                await model_image_file.seek(0)

            # Combine results from both APIs
            combined_result = {
                "success": True,
                "message": "Model created successfully",
                "api1_data": api1_result,
                "api2_data": api2_result,
                "combined_score": (api1_result["score"] + api2_result["confidence"]) / 2
            }

            return combined_result
            
        except Exception as e:
            print(f"Error in create_model: {str(e)}")
            raise e
# class ProjectService:
#     @staticmethod
#     async def get_user_projects(user_id: str):
#         """
#         Get all projects for a user
#         """
#         try:
#             print(f"Getting projects for user: {user_id}")
#             db = await get_database()
#             # Use db directly like in create_project
#             projects = await db["projects"].find(
#                 {"user_id": user_id}
#             ).to_list(length=None)
            
#             print(f"Found projects: {projects}")
            
#             # Convert ObjectId to string for JSON serialization
#             for project in projects:
#                 project["id"] = str(project["_id"])
#                 del project["_id"]
#                 # Make sure name field exists
#                 if "project_name" in project:
#                     project["name"] = project["project_name"]
#                     del project["project_name"]
                
#             return projects
#         except Exception as e:
#             print(f"Error in get_user_projects: {str(e)}")
#             raise e

#     @staticmethod
#     async def delete_project(project_id: str):
#         """
#         Delete a project
#         """
#         db = await get_database()
#         result = await db["projects"].delete_one(
#             {"_id": ObjectId(project_id)}
#         )
#         if result.deleted_count:
#             return {"message": "Project deleted successfully"}
#         return {"message": "Project not found"}

#     @staticmethod
#     async def create_project(user_id: str, project_name: str, collaborators: List[str], is_public: bool):
#         """
#         Create a new project
#         """
#         try:
#             db = await get_database()
#             project = {
#                 "user_id": user_id,
#                 "name": project_name,  # Changed from project_name to name to match schema
#                 "created_at": datetime.utcnow(),
#                 "is_public": is_public,
#                 "collaborators": collaborators,
#                 "chat_history": []
#             }
#             result = await db["projects"].insert_one(project)
            
#             # Return the created project
#             created_project = await db["projects"].find_one({"_id": result.inserted_id})
#             created_project["id"] = str(created_project["_id"])
#             del created_project["_id"]
            
#             return created_project
#         except Exception as e:
#             print(f"Error in create_project: {str(e)}")
#             raise e

#     @staticmethod
#     async def get_one(project_id: str):
#         """
#         Get a project and all its attributes
#         """
#         try:
#             db = await get_database()
#             project = await db["projects"].find_one({"_id": ObjectId(project_id)})
#             if project:
#                 # Convert ObjectId to string for JSON serialization
#                 project["id"] = str(project["_id"])
#                 del project["_id"]
                
#                 # Ensure all dates are serializable
#                 if "created_at" in project:
#                     project["created_at"] = project["created_at"].isoformat()
                    
#                 print("Found project:", project)
#                 return project
#             else:
#                 print("No project found with id:", project_id)
#                 return None
#         except Exception as e:
#             print(f"Error in get_one: {str(e)}")
#             raise e

#     @staticmethod
#     async def save_chat(project_id: str, chat_history: List[Dict[str, Any]]):
#         """
#         Save the chat history for a project
#         """
#         try:
#             db = await get_database()
#             result = await db["projects"].update_one(
#                 {"_id": ObjectId(project_id)},
#                 {"$set": {"chat_history": chat_history}}
#             )
#             return {"message": "Chat history saved successfully"}
#         except Exception as e:
#             print(f"Error in save_chat: {str(e)}")
#             raise e

