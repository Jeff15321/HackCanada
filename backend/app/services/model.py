import json
from typing import Dict, Any, Optional
from fastapi import UploadFile
import random
import asyncio
from openai import AsyncOpenAI
import os
import base64
from dotenv import load_dotenv
from app.core.database import get_database
from datetime import datetime
from fastapi import HTTPException
from pathlib import Path
import shutil
from bson import ObjectId
import aiohttp

# Load environment variables
load_dotenv()

# Initialize OpenAI client properly
openai_client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Add this at the top of the file
UPLOAD_DIR = Path("uploads/images")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

prompt = """
You are a plant health analysis expert. Your task is to analyze a flower's condition based on an image input and provide your insights in a JSON formatted string that exactly matches the schema below. Do not include any additional commentary or text outside of the JSON string.

The JSON schema is as follows:

{
  "glbFileUrl": string,
  "parameters": {
    "colorVibrancy": {
      "score": int,
      "explanation": string
    },
    "leafAreaIndex": {
      "score": int,
      "explanation": string
    },
    "wilting": {
      "score": int,
      "explanation": string
    },
    "spotting": {
      "score": int,
      "explanation": string
    },
    "symmetry": {
      "score": int,
      "explanation": string
    }
  },
  "name": string,
  "walletID": string,
  "price": int,
  "special": [
    {
      "attribute": string,
      "rarity": int
    }
  ]
}

For each field, follow these guidelines:

1. **glbFileUrl:**  
     - leave blank
2. **parameters:**  
   This object contains detailed analyses of specific health indicators:
   
   - **colorVibrancy:**  
     - Evaluate the intensity, saturation, and uniformity of the flower's colors.
     - Write a two-sentence explanation discussing the brightness, vividness, and any fading or color inconsistencies.
     - Assign an integer score where a higher score represents excellent color vibrancy.
     
   - **leafAreaIndex:**  
     - Assess the density and coverage of the leaves relative to the flower.
     - Write a two-sentence explanation that describes whether the foliage is abundant and how it contributes to the overall health.
     - Assign an integer score where a higher score indicates an optimal leaf area.
     
   - **wilting:**  
     - Determine if there are any signs of wilting, such as drooping or sagging petals and leaves.
     - Write a two-sentence explanation detailing whether the tissues are firm and hydrated or showing signs of dehydration and drooping.
     - Assign an integer score where a higher score indicates minimal or no wilting.
     
   - **spotting:**  
     - Identify any spots, blemishes, or discolorations that may signal disease or pest damage.
     - Write a two-sentence explanation describing the severity and distribution of any spotting observed.
     - Assign an integer score where a higher score indicates fewer or negligible spotting issues.
     
   - **symmetry:**  
     - Evaluate the overall symmetry of the flower, including the arrangement of petals, leaves, and stem.
     - Write a two-sentence explanation discussing whether the structure is balanced and regular or irregular and disorganized.
     - Assign an integer score where a higher score indicates greater symmetry.

3. **name:**  
   - Provide a string representing the name of the flower or the product derived from it.

4. **walletID:**  
   - Provide a string that represents the wallet ID associated with this analysis or transaction.

5. **price:**  
   - Provide an integer representing the price of the product, analysis, or associated item.
6. **special:**
   - Provide an array of objects with the following properties:
     - **attribute:** string, the attribute of the flower
     - **rarity:** integer, the rarity of the attribute from 1 to 5

Try to keep the attribute's percentage values from 50% to 70%, but if you think they excel in that field, dont hold back to give very high percentage.
**Examples:**
Below are three examples of correctly formatted outputs:

### Example 1: Healthy Flower Analysis
**Image Description:**  
The image shows a vibrant red rose in full bloom. The petals are evenly arranged and glossy with visible dewdrops, supported by lush green leaves and a strong, upright stem. The softly blurred background emphasizes the flower's vivid color and intricate details.

"
{"glbFileUrl":"","parameters":{"colorVibrancy":{"score":85,"explanation":"The red hue is rich and vibrant, complemented by subtle shading that enhances depth and freshness."},"leafAreaIndex":{"score":85,"explanation":"The foliage is dense, contributing to strong photosynthetic capability and a balanced aesthetic."},"wilting":{"score":97,"explanation":"No signs of wilting; petals and leaves appear fresh and well-hydrated."},"spotting":{"score":90,"explanation":"No visible blemishes or spots, indicating excellent health and optimal environmental conditions."},"symmetry":{"score":80,"explanation":"The petals and leaves are arranged in a near-perfect symmetrical pattern, reflecting strong genetic traits."}},"name":"Radiant Scarlet Rose","walletID":"0xDEF123ABC456XYZ789","price":250,"special":[{"attribute":"Rare Fragrance","rarity":5},{"attribute":"High Petal Count","rarity":4}]}
"

### Example 2: Moderately Healthy Flower Analysis
**Image Description:**  
A sunflower with bright yellow petals, slightly curled at the edges. The center is well-defined, but a few leaves show minor signs of damage. The background features a bright blue sky.

"
{"glbFileUrl":"","parameters":{"colorVibrancy":{"score":50,"explanation":"The yellow petals are vivid, though slight fading is visible at the tips."},"leafAreaIndex":{"score":60,"explanation":"Leaf coverage is sufficient but not dense; some minor gaps are present."},"wilting":{"score":60,"explanation":"Most petals are firm, but the edges of a few show curling."},"spotting":{"score":55,"explanation":"A few minor brown spots on the lower leaves indicate slight environmental stress."},"symmetry":{"score":57,"explanation":"The overall form is well-balanced, but a few petals are slightly uneven."}},"name":"Golden Helios Sunflower","walletID":"0x887XYZ654DEF321ABC","price":80,"special":[{"attribute":"High Sun Resistance","rarity":3},{"attribute":"Large Seed Head","rarity":2}]}
"

### Example 3: Unhealthy Flower Analysis
**Image Description:**  
A pale, wilted flower with drooping petals and a visibly weakened stem. The background is dull and low-contrast, emphasizing signs of decay such as brown patches and uneven discoloration.

"
{"glbFileUrl":"","parameters":{"colorVibrancy":{"score":30,"explanation":"The color is faded, with noticeable discoloration and brown patches on the petals."},"leafAreaIndex":{"score":40,"explanation":"The leaf coverage is sparse, with significant gaps due to withering."},"wilting":{"score":20,"explanation":"Petals and leaves appear shriveled and drooping, indicating severe dehydration."},"spotting":{"score":25,"explanation":"Dark spots and necrotic patches indicate signs of disease or pest infestation."},"symmetry":{"score":35,"explanation":"The petals and leaves are asymmetrically arranged, suggesting poor growth conditions."}},"name":"Faded Elegance Lily","walletID":"0x654XYZ987DEF321ABC","price":30,"special":[{"attribute":"Unusual Petal Curling","rarity":2}]}
"
Return only the final JSON string as your output.

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
            db = await get_database()
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

                    contents = await model_image_file.read()
                    base64_image = base64.b64encode(contents).decode('utf-8')
                    await model_image_file.seek(0)

                    # Use openai_client instead of client
                    response = await openai_client.chat.completions.create(
                        model="gpt-4o-mini",
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

                    analysis = response.choices[0].message.content
                    return {
                        "api2_result": "success",
                        "analysis": analysis,
                        "confidence": random.randint(70, 90)
                    }
                except Exception as e:
                    print(f"Error in ChatGPT API call: {str(e)}")
                    return {
                        "api2_result": "error",
                        "analysis": str(e),
                        "confidence": 0
                    }

            api1_result, api2_result = await asyncio.gather(
                api_call_1(),
                chat_gpt_analysis()
            )

            # Parse GPT response into JSON
            try:
                # Clean the markdown formatting if present
                analysis_text = api2_result["analysis"]
                clean_json = analysis_text.replace("```json\n", "").replace("\n```", "").strip()
                analysis_data = json.loads(clean_json)

                # Save the uploaded file
                if model_image_file:
                    # Create a unique filename
                    file_extension = Path(model_image_file.filename).suffix
                    unique_filename = f"{datetime.utcnow().timestamp()}{file_extension}"
                    file_path = UPLOAD_DIR / unique_filename
                    
                    # Save the file
                    with file_path.open("wb") as buffer:
                        contents = await model_image_file.read()
                        buffer.write(contents)
                    await model_image_file.seek(0)
                    
                    # Update the URL to point to our saved file
                    saved_image_url = f"/uploads/images/{unique_filename}"
                else:
                    saved_image_url = imageUrl

                # Transform into MongoDB document with the required schema
                model_doc = {
                    "glbFileUrl": saved_image_url,
                    "parameters": {
                        "colorVibrancy": analysis_data.get("parameters", {}).get("colorVibrancy", {"score": 0, "explanation": ""}),
                        "leafAreaIndex": analysis_data.get("parameters", {}).get("leafAreaIndex", {"score": 0, "explanation": ""}),
                        "wilting": analysis_data.get("parameters", {}).get("wilting", {"score": 0, "explanation": ""}),
                        "spotting": analysis_data.get("parameters", {}).get("spotting", {"score": 0, "explanation": ""}),
                        "symmetry": analysis_data.get("parameters", {}).get("symmetry", {"score": 0, "explanation": ""})
                    },
                    "name": model_name or analysis_data.get("name", ""),
                    "walletID": userId,
                    "price": analysis_data.get("price", 0),
                    "special": analysis_data.get("special", []),
                    "created_at": datetime.utcnow(),
                    "combined_score": (api1_result["score"] + api2_result["confidence"]) / 2
                }

                # Save to MongoDB
                result = await db.models.insert_one(model_doc)

            except json.JSONDecodeError as e:
                print(f"Error parsing GPT response as JSON: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to parse GPT analysis")

            # Return response with MongoDB ID and saved image URL
            combined_result = {
                "success": True,
                "message": "Model created successfully",
                "model_id": str(result.inserted_id),
                "saved_image_url": saved_image_url,
                "api1_data": api1_result,
                "api2_data": api2_result,
                "combined_score": model_doc["combined_score"],
                "gpt_analysis": analysis_data
            }

            return combined_result

        except Exception as e:
            print(f"Error in create_model: {str(e)}")
            raise e

    @staticmethod
    async def get_all_models():
        try:
            db = await get_database()
            cursor = db.models.find({})
            models = await cursor.to_list(length=100)
            
            # Convert ObjectId to string and format response
            formatted_models = []
            for model in models:
                model['_id'] = str(model['_id'])  # Convert ObjectId to string
                formatted_models.append({
                    "glbFileUrl": model.get("glbFileUrl", ""),  # This should be the saved file path
                    "parameters": model.get("parameters", {}),
                    "name": model.get("name", ""),
                    "walletID": model.get("walletID", ""),
                    "price": model.get("price", 0),
                    "special": model.get("special", []),
                    "id": model['_id'],
                    "created_at": model.get("created_at", "")
                })
            
            print("Returning models with URLs:", [m["glbFileUrl"] for m in formatted_models])  # Debug print
            return formatted_models
        except Exception as e:
            print(f"Error fetching models: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))

    @staticmethod
    async def update_owner(model_id: str, new_owner_id: str):
        try:
            db = await get_database()
            
            # Check if model exists
            model = await db.models.find_one({"_id": ObjectId(model_id)})
            if not model:
                raise HTTPException(status_code=404, detail="Model not found")
            
            # Update the owner
            result = await db.models.update_one(
                {"_id": ObjectId(model_id)},
                {"$set": {"walletID": new_owner_id}}
            )
            
            if result.modified_count == 0:
                raise HTTPException(status_code=400, detail="Failed to update owner")
            
            return {
                "success": True,
                "message": "Owner updated successfully"
            }
        except Exception as e:
            print(f"Error updating owner: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))


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

        response = await openai_client.chat.completions.create(
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

