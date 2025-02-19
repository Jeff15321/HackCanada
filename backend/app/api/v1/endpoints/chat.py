from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import sys
from pathlib import Path

# Add both version5 and version5/src to Python path
root_dir = Path(__file__).resolve().parents[5]
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / 'version5'))
sys.path.append(str(root_dir / 'version5' / 'src'))
sys.path.append(str(root_dir / 'version5' / 'documents'))

print(f"Python path includes: {sys.path}")

from version5.run import process_task

router = APIRouter()

@router.post("/process")
async def process_message(message: Dict[str, Any]):
    try:
        result = await process_task(message.get("content", ""))
        return {"response": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
