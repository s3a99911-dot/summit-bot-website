from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SUMMIT BOT"
    app_env: str = "development"
    database_url: str = "sqlite:///./summit_bot.db"
    discord_client_id: str = ""
    discord_client_secret: str = ""
    discord_redirect_uri: str = "http://localhost:8000/auth/callback"
    secret_key: str = "change-me-in-production"
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origin_list(self):
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
