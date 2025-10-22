from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    #Database
    DATABASE_URL: str="postgresql://user:password@localhost/dbname"

    #Security
    SECRET_KEY: str="kjsflkBKL HLKJLHfhklf32ou4oppdjsbf"
    ALGORITHM: str="H256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int=30 

    #Redis
    REDIS_URL: str="redis://localhost:6379"

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Banking Management System"
    
    # Email (for notifications)
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()