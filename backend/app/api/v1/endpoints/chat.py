from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import sys
import shutil
from pathlib import Path
import traceback

# Add both version5 and version5/src to Python path
root_dir = Path(__file__).resolve().parents[5]
sys.path.append(str(root_dir))
sys.path.append(str(root_dir / 'version5'))
sys.path.append(str(root_dir / 'version5' / 'src'))

from version5.run import process_task

router = APIRouter()

# Get absolute paths
BACKEND_DIR = Path(__file__).resolve().parents[3]  # backend/
DOCUMENTS_DIR = BACKEND_DIR / "documents"
RUBRIC_FILE = DOCUMENTS_DIR / "Critical Essay Rubric.pdf"
ENSMENGER_FILE = DOCUMENTS_DIR / "Ensmenger2018.pdf"

# Create documents directory if it doesn't exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)

# Copy PDF files from version5/documents to backend/documents if they don't exist
VERSION5_DOCS = root_dir / "version5" / "documents"
if VERSION5_DOCS.exists():
    if not RUBRIC_FILE.exists() and (VERSION5_DOCS / "Critical Essay Rubric.pdf").exists():
        shutil.copy2(VERSION5_DOCS / "Critical Essay Rubric.pdf", RUBRIC_FILE)
    if not ENSMENGER_FILE.exists() and (VERSION5_DOCS / "Ensmenger2018.pdf").exists():
        shutil.copy2(VERSION5_DOCS / "Ensmenger2018.pdf", ENSMENGER_FILE)

@router.post("/process")
def chat_endpoint(message: Dict[str, Any]):
    """
    Chat endpoint that processes messages and returns responses
    """
    return {"response": "Hello, world!"}
