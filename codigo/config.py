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
    LANGFUSE_PUBLIC_KEY: str = Field(default="")
    LANGFUSE_SECRET_KEY: str = Field(default="")
    LANGFUSE_HOST: str = Field(default="https://us.cloud.langfuse.com")

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(__file__), ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

try:
    settings = Settings()
    # Inyectar claves de Langfuse en os.environ para que el SDK de Langfuse las lea automáticamente
    if settings.LANGFUSE_PUBLIC_KEY and settings.LANGFUSE_SECRET_KEY:
        os.environ["LANGFUSE_PUBLIC_KEY"] = settings.LANGFUSE_PUBLIC_KEY
        os.environ["LANGFUSE_SECRET_KEY"] = settings.LANGFUSE_SECRET_KEY
        os.environ["LANGFUSE_HOST"] = settings.LANGFUSE_HOST
except Exception:
    settings = Settings(DEMO_MODE=False)
