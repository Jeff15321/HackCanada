from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
async def test_endpoint():
    return {
        "message": "Hello sd dfgfxcvgdsFastAPI!",
        "status": "success"
    } 