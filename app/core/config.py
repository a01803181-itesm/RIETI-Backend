from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "RIETI API"

    MYSQL_DB_HOST: str
    MYSQL_DB_PASSWORD: str
    MYSQL_DB_NAME: str
    MYSQL_DB_USER: str
    MYSQL_DB_PORT: str

    ALLOWED_ORIGINS: list[str] = ['*']

    model_config = SettingsConfigDict(
        env_file=os.getenv("ENV_FILE", ".env"),
        extra="ignore"
    )

settings = Settings()