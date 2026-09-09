import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(default="tu_api_key_aquí")
    GEMINI_MODEL: str = Field(default="gemini-3.5-flash") # gemini-3.5-flash, gemini-2.5-flash, etc.
    DEMO_MODE: bool = Field(default=False) # Configurado por defecto a False para usar Gemini Real!
    API_KEY: str = Field(default="trading-secret-key-123")
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

try:
    settings = Settings()
except Exception:
    settings = Settings(DEMO_MODE=False)
