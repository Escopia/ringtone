from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/ringtone_db"
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

settings = Settings()
