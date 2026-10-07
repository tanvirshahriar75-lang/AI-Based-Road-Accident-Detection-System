from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "AI-Based Road Accident Detection System"
    app_env: str = "development"
    debug: bool = True
    database_url: str = "sqlite:///./accident_detection.db"
    secret_key: str = "change-this-development-secret"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    max_upload_size_mb: int = 200

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
