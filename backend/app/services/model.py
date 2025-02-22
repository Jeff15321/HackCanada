import json
from typing import Dict, Any, Optional
from fastapi import UploadFile
import random
import asyncio
from openai import AsyncOpenAI, OpenAI
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

prompt = """
You are a plant health analysis expert. Provide insights about flower health based on the image input based on the following criteria:

1. Shape & Structure: Evaluate the overall form, symmetry, and arrangement of the flower's components (petals, leaves, and stem). Instruct the agent to note any irregularities, deformations, or drooping that could indicate stress or damage.

2. Color & Texture: Analyze the dominant colors, gradients, and surface patterns. Tell the agent to look for uniformity and vibrancy as well as any signs of discoloration, rough textures, or patches that may point to issues.

3. Health: Direct the agent to identify signs of disease, pest infestation, or environmental damage. This includes detecting spots, necrosis, wilting, or other abnormalities in the tissue.

4. Development Stage: Determine whether the flower is a bud, fully bloomed, or wilting. Instruct the agent to correlate the developmental stage with overall vitality, as deviations from expected growth stages might indicate underlying problems.

please provide a two sentence analysis of each criteria and also rate the flower from 0% to 100% for each criteria.

please return the analysis in a json format.

Example 1: Healthy Flower Analysis
Image Input Description:
The image shows a vibrant red rose in full bloom. The petals are evenly arranged and glossy with visible dewdrops, supported by lush green leaves and a strong, upright stem. The softly blurred background emphasizes the flower's vivid color and intricate details.
{
  "Shape & Structure": {
    "analysis": "The flower exhibits a balanced and symmetrical form with uniformly arranged petals and a robust stem. The well-defined structure of the petals and leaves reflects strong genetic traits and optimal growth conditions.",
    "rating": "95%"
  },
  "Color & Texture": {
    "analysis": "The dominant vibrant red hue is complemented by subtle shading that adds depth, and the glossy surface indicates excellent hydration. The uniform, smooth texture underscores the flower's healthy condition.",
    "rating": "93%"
  },
  "Health": {
    "analysis": "There are no visible signs of disease, discoloration, or pest damage; the tissues are firm and resilient. The overall appearance confirms that the flower is thriving in a favorable environment.",
    "rating": "96%"
  },
  "Development Stage": {
    "analysis": "The flower is captured in full bloom with all petals unfurled, highlighting its reproductive peak. This mature stage is ideal for attracting pollinators and signifies optimal aesthetic and physiological condition.",
    "rating": "95%"
  }
}

Example 2: Unhealthy Flower Analysis
Image Input Description:
The image depicts a pale, wilted flower with drooping petals and a visibly weakened stem. The background is dull and low-contrast, emphasizing the lack of vibrancy and clear signs of decay such as brown patches and uneven discoloration.
{
  "Shape & Structure": {
    "analysis": "The flower exhibits an irregular, asymmetrical form with drooping, misshapen petals and a weakened stem. The disorganized structure suggests significant physical stress and poor growth conditions.",
    "rating": "35%"
  },
  "Color & Texture": {
    "analysis": "The overall color is muted and faded, with brown patches and uneven hues indicating a loss of vitality. The texture is rough and brittle, reflecting dehydration and the early stages of decay.",
    "rating": "30%"
  },
  "Health": {
    "analysis": "Obvious signs of distress, such as necrotic spots and widespread discoloration, indicate that the flower is affected by disease or pest infestation. The fragile, compromised tissue further confirms its poor health.",
    "rating": "25%"
  },
  "Development Stage": {
    "analysis": "The flower appears wilted with partially closed or disintegrating petals, demonstrating a decline from its optimal bloom stage. This advanced stage of deterioration reflects prolonged exposure to adverse conditions.",
    "rating": "20%"
  }
}
"""

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

            async def api_call_1():
                await asyncio.sleep(1)
                return {
                    "api1_result": "success",
                    "score": random.randint(0, 100)
                }

            async def chat_gpt_analysis():
                try:
                    if not model_image_file:
                        return {
                            "api2_result": "error",
                            "analysis": "No image file provided",
                            "confidence": 0
                        }

                    # Read image file
                    contents = await model_image_file.read()
                    base64_image = base64.b64encode(contents).decode('utf-8')
                    await model_image_file.seek(0)

                    print("Sending request to OpenAI API...")

                    # Use the vision model and include the base64 image string in the request
                    response = await client.chat.completions.create(
                        model="gpt-4o-mini",  # Use a model with vision capabilities
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "text",
                                        "text": prompt
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{base64_image}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=300
                    )

                    print("Received response from OpenAI API")

                    analysis = response.choices[0].message.content

                    try:
                        import re
                        scores = re.findall(r'(\d{1,3})/100|score.*?(\d{1,3})|health.*?(\d{1,3})', analysis.lower())
                        confidence = int(scores[0][0]) if scores else random.randint(70, 90)
                    except:
                        confidence = random.randint(70, 90)

                    return {
                        "api2_result": "success",
                        "analysis": analysis,
                        "confidence": confidence
                    }
                except Exception as e:
                    print(f"Error in ChatGPT API call: {str(e)}")
                    return {
                        "api2_result": "error",
                        "analysis": f"Failed to analyze image: {str(e)}",
                        "confidence": 0
                    }

            api1_result, api2_result = await asyncio.gather(
                api_call_1(),
                chat_gpt_analysis()
            )

            print("API 1 Result:", api1_result)
            print("API 2 Result (ChatGPT):", api2_result)

            if model_image_file:
                contents = await model_image_file.read()
                print(f"Image file size: {len(contents)} bytes")
                await model_image_file.seek(0)

            combined_result = {
                "success": True,
                "message": "Model created successfully",
                "api1_data": api1_result,
                "api2_data": api2_result,
                "combined_score": (api1_result["score"] + api2_result["confidence"]) / 2,
                "gpt_analysis": api2_result.get("analysis", "No analysis available")
            }

            return combined_result
            
        except Exception as e:
            print(f"Error in create_model: {str(e)}")
            raise e

def encode_image(image_path: str) -> str:
    """
    Reads a local image file and returns a Base64-encoded string.
    """
    import base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

async def analyze_local_image(image_path: str):
    """
    Example function to encode a local image and send it
    with a 'gpt-4o-mini' vision model request.
    """
    # Get the Base64-encoded string
    base64_image = encode_image(image_path)

    try:
        print("Sending request to OpenAI for image analysis...")

        response = await client.chat.completions.create(
            model="gpt-4o-mini",  # Ensure you have access to a vision-capable model
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "What is in this image?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                # Provide a data URL with the Base64-encoded content
                                "url": f"data:image/jpeg;base64,{base64_image}",
                                # Optionally set detail level: 'low', 'high', or leave it 'auto'
                                # "detail": "high"
                            }
                        }
                    ]
                }
            ],
            max_tokens=300,
        )

        print("Received response from OpenAI API")
        analysis = response.choices[0].message.content
        print("Analysis:", analysis)
        return analysis

    except Exception as e:
        print(f"Error in ChatGPT API call: {str(e)}")
        return f"Failed to analyze image: {str(e)}"

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

