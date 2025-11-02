from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./ringtone.db")
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "your-secret-key-change-in-production"
    aws_access_key_id: str = ""
    aws_secret_access_key: str = ""
    s3_bucket: str = "ringtone-audio-files"
    mtn_consumer_key: str = ""
    mtn_consumer_secret: str = ""
    mtn_api_url: str = "https://api.mtn.com/v1"
    
    class Config:
        env_file = ".env"

try:
    settings = Settings()
except:
    class Settings:
        database_url = "sqlite:///./ringtone.db"
        redis_url = "redis://localhost:6379/0"
        secret_key = "dev-secret-key"
        aws_access_key_id = ""
        aws_secret_access_key = ""
        s3_bucket = "ringtone-audio-files"
        mtn_consumer_key = ""
        mtn_consumer_secret = ""
        mtn_api_url = "https://api.mtn.com/v1"
    settings = Settings()
