from pydantic_settings import BaseSettings
from typing import List
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/v1"
    PROJECT_NAME: str = "FastAPI Project"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "A FastAPI project with proper structure"
    
    # Server settings
    ALLOWED_HOSTS: str
    CORS_ALLOWED_ORIGINS: str
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React/Next.js frontend
        "http://127.0.0.1:3000"
    ]
    
    # LangSmith
    LANGSMITH_TRACING: bool = True
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    
    # OpenAI
    OPENAI_API_KEY: str
    
    # MongoDB settings
    MONGODB_URL: str
    MONGODB_DB_NAME: str

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings() 