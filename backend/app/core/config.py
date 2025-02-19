from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "A FastAPI project with proper structure"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # LangSmith
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    
    # OpenAI
    OPENAI_API_KEY: str

    class Config:
        env_file = ".env"

settings = Settings() 