from functools import lru_cache, cached_property

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="src/core/settings/.env", env_file_encoding="utf-8")

    db_user: str
    db_password: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str

    secret_key: str
    media_path: str
    debug: bool = False

    broker_url: str  = "amqp://celery:celerypassword@localhost:5672/celeryvhost"


    @cached_property
    def result_backend(self) -> str:
        return "db+" + self.database_sync_url

    @cached_property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
