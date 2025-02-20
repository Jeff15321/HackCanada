from fastapi import APIRouter, HTTPException
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth import AuthService

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """
    Login endpoint that accepts any credentials for testing
    """
    try:
        return await AuthService.login(request.username, request.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 