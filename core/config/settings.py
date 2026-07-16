from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_URL_AUTH: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    API_KEY: str # Para comunicación interna

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
