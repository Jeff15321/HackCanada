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
