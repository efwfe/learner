from pydantic_settings import BaseSettings
from typing import Optional
import os

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "Learner - 智能学习管理系统"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 数据库配置
    DATABASE_URL: str = "sqlite:///./learner.db"
    
    # Azure OpenAI 配置
    AZURE_OPENAI_ENDPOINT:str = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_API_KEY: str = os.environ.get("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_DEPLOYMENT_NAME: str = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    AZURE_OPENAI_API_VERSION: str =  os.environ.get("AZURE_OPENAI_API_VERSION")
    
    # CORS 配置
    BACKEND_CORS_ORIGINS: list[str] = ["http://localhost:3001", "http://localhost:3000"]
    
    # JWT 配置（如果需要用户认证）
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
