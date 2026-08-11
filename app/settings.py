from dotenv import find_dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(usecwd=True), env_file_encoding='utf-8'
    )

    DATABASE_URL: PostgresDsn
    IPV4_DATABASE_URL: PostgresDsn | None = None
    DEBUG_SQL: bool = Field(init=False)
    SENTRY_DSN: str | None = None


settings = Settings()
