from fastapi import APIRouter, HTTPException
import httpx
import json
from typing import Dict, Any
import aiohttp

router = APIRouter()

BASE_URL = 'https://72ddc6f7069330b4c304c2f4e662bd321785dd91-3000.dstack-prod5.phala.network'

async def mint_nft(client: httpx.AsyncClient, model_data: Dict[str, Any]) -> Dict[str, Any]:
    token_id = f"plant-tee-{model_data.get('id', '14')}"
    mint_payload = {
        "token_id": token_id,
        "receiver_id": model_data.get("walletID", "hackcanada.testnet"),
        "plant_metadata": {
            "glb_file_url": model_data.get("glbFileUrl"),
            "parameters": model_data.get("parameters", {}),
            "name": model_data.get("name", "TEE Plant"),
            "wallet_id": model_data.get("walletID", "hackcanada.testnet"),
            "price": str(model_data.get("price", "100000"))
        }
    }
    
    print("Mint Payload:", json.dumps(mint_payload, indent=2))
    mint_response = await client.post(f"{BASE_URL}/api/nft/mint", json=mint_payload)
    mint_result = mint_response.json()
    print("Mint Response:", json.dumps(mint_result, indent=2))
    return mint_result

async def get_owner_tokens(client: httpx.AsyncClient, wallet_id: str) -> Dict[str, Any]:
    print(f"Calling /api/nft/tokens/{wallet_id}...")
    owner_tokens_response = await client.get(f"{BASE_URL}/api/nft/tokens/{wallet_id}")
    owner_tokens_result = owner_tokens_response.json()
    print(f"Tokens for {wallet_id}:", owner_tokens_result)
    return owner_tokens_result

async def run_pipeline(data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        # Use the data passed from frontend
        test_payload = {
            "token_id": data["token_id"],
            "receiver_id": data["receiver_id"],
            "plant_metadata": {
                "glb_file_url": data["plant_metadata"]["glb_file_url"],
                "parameters": {
                    "color_vibrancy": data["plant_metadata"]["parameters"]["color_vibrancy"],
                    "leaf_area_index": data["plant_metadata"]["parameters"]["leaf_area_index"],
                    "wilting": data["plant_metadata"]["parameters"]["wilting"],
                    "spotting": data["plant_metadata"]["parameters"]["spotting"],
                    "symmetry": data["plant_metadata"]["parameters"]["symmetry"]
                },
                "name": data["plant_metadata"]["name"],
                "wallet_id": data["plant_metadata"]["wallet_id"],
                "price": data["plant_metadata"]["price"]
            }
        }

        # Make a request to the Phala network endpoint
        async with aiohttp.ClientSession() as session:
            phala_url = 'https://72ddc6f7069330b4c304c2f4e662bd321785dd91-3000.dstack-prod5.phala.network/api/nft/mint'
            async with session.post(phala_url, json=test_payload) as response:
                result = await response.json()
                print('Mint NFT result:', result)
                return result

    except Exception as e:
        print(f"Error in run_pipeline: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/run")
async def run_pipeline_endpoint(data: Dict[str, Any]):
    """
    Run the pipeline with the provided data
    """
    return await run_pipeline(data)

@router.post("/v1/nft/mint")
async def mint_nft_endpoint(model_data: dict):
    try:
        async with httpx.AsyncClient() as client:
            result = await mint_nft(client, model_data)
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/v1/nft/tokens/{wallet_id}")
async def get_owner_tokens_endpoint(wallet_id: str):
    try:
        async with httpx.AsyncClient() as client:
            result = await get_owner_tokens(client, wallet_id)
            print("Token response structure:", result)  # Debug log
            return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))