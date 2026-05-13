import os
from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
# En producción, .env no existirá, por lo que load_dotenv falla silenciosamente,
# pero Pydantic leerá de las variables de entorno del sistema.
load_dotenv()

class Settings(BaseSettings):
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_USER: str = os.getenv("GITHUB_USER", "Alejandro-78G")
    APP_TITLE: str = "Alejandro Cristancho — Data Analyst Portfolio"
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "False").lower() in ("true", "1", "t")
    GITHUB_API_BASE: str = "https://api.github.com"
    CACHE_TTL_SECONDS: int = 300  # 5 min cache para GitHub API

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
