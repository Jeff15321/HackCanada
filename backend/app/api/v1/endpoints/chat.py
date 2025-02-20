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
    try:
        print(f"Received message: {message}")
        
        # Verify files exist
        if not RUBRIC_FILE.exists():
            raise HTTPException(
                status_code=500, 
                detail=f"Required file not found: {RUBRIC_FILE}"
            )
        if not ENSMENGER_FILE.exists():
            raise HTTPException(
                status_code=500,
                detail=f"Required file not found: {ENSMENGER_FILE}"
            )
        #TODO: import supporting pdf files correctly, it is static right now
        #TODO: currently, I use the hardcoded prompt_text. When the AI people finish the prompt engineering, make a API rout that sends to the prompt engineering to fetch for a better prompt and set that as the prompt_text
        #TODO: it also says RAG is not working, so we need to fix that
        #TODO: it always outputs environment related variables, can you try to change the documents and test it again?
        # Use hardcoded prompt_text instead of message content
        prompt_text = f"""
        Task: Write a comprehensive analytical report on League of Legends, examining its gameplay mechanics, competitive ecosystem, and cultural impact.

        Required Components:
        1. Game Overview (500-600 words)
        - Explain the core gameplay mechanics and objectives
        - Describe the role-based team composition system
        - Detail the map structure and key strategic elements
        - Outline the free-to-play business model and monetization strategy

        2. Champion Analysis (800-1000 words)
        - Examine the champion classification system (fighters, mages, tanks, etc.)
        - Analyze champion design philosophy and evolution over time
        - Discuss the meta game and how it influences champion viability
        - Evaluate the balance between new and classic champions

        3. Competitive Ecosystem (700-900 words)
        - Detail the structure of professional leagues (LCS, LEC, LCK, LPL)
        - Analyze the World Championship format and its significance
        - Examine the path-to-pro system and amateur scene
        - Discuss the impact of esports on game development

        4. Game Systems (800-1000 words)
        - Evaluate the ranking and matchmaking systems
        - Analyze the rune and item systems
        - Examine the progression and reward mechanisms
        - Discuss seasonal changes and their impact on gameplay

        5. Community and Culture (600-800 words)
        - Analyze player behavior and community dynamics
        - Examine the impact of streaming and content creation
        - Discuss regional playing styles and server differences
        - Evaluate community feedback and developer response

        6. Technical Analysis (400-500 words)
        - Examine game engine capabilities and limitations
        - Analyze network infrastructure and performance
        - Discuss client-server architecture
        - Evaluate graphics and sound design

        Requirements:
        - Use precise gaming terminology
        - Include specific examples and statistics
        - Analyze patch history and meta evolution
        - Consider both casual and competitive perspectives
        - Reference official game data and professional matches
        - Total length: 3800-4800 words

        Additional Guidelines:
        - Include win rates and pick rates where relevant
        - Analyze current meta trends and historical changes
        - Consider the new player experience
        - Examine both high and low-level play
        - Compare with other games in the MOBA genre
        - Discuss future development possibilities
        """

        # Process the chat message
        response = process_task(
            prompt=prompt_text,
            instructional_pdf_path=str(RUBRIC_FILE),
            supplementary_files=[str(ENSMENGER_FILE)]
        )
                
        if response is None:
            raise HTTPException(status_code=500, detail="Process task returned None")
            
        if not isinstance(response, dict):
            raise HTTPException(status_code=500, detail=f"Expected dict response but got {type(response)}")
            
        if 'merged_result_with_agent' not in response:
            raise HTTPException(
                status_code=500, 
                detail=f"Response missing merged_result_with_agent. Keys: {response.keys() if isinstance(response, dict) else 'not a dict'}"
            )
        return response

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        print("Traceback:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
