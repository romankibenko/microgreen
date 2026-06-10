from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    bot_token: str | None = None
    backend_url: str = "http://backend:8000"
    shop_url: str = "http://localhost:5173"


settings = Settings()
