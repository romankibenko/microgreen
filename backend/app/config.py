from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: str
    # 5173 — лендинг, 5174 — админка (dev-серверы Vite).
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:5174"]

    # Telegram (бэкенд шлёт уведомления о заказах). Без токена нотификатор молчит.
    bot_token: str | None = None
    admin_chat_id: int | None = None
    shop_url: str = "http://localhost:5173"

    # Ежедневный дайджест по посадкам: час (по digest_tz) и часовой пояс.
    digest_hour: int = 9
    digest_tz: str = "Europe/Moscow"

    # Админка: JWT + сидинг первого админа из .env при старте.
    jwt_secret: str = "change-me-in-prod"
    jwt_expire_minutes: int = 1440
    admin_username: str | None = None
    admin_password: str | None = None


settings = Settings()
