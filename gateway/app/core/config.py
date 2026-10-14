from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    env: str = "production"
    postgres_password: str
    redis_url: str = "redis://redis:6379/0"
    jwt_signing_key: str
    jwt_access_ttl_min: int = 15
    jwt_refresh_ttl_days: int = 30
    marzban_api_url: str = "http://host.docker.internal:8000"
    marzban_api_user: str
    marzban_api_password: str

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://vpn:{self.postgres_password}@postgres:5432/vpn"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
