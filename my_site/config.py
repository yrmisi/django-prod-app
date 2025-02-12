"""
This module contains the configuration settings for the application.

It uses Pydantic to load environment variables from a .env file.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class uses Pydantic to load environment variables from a specified
    .env file.
    """

    data_source_name: str | None = None
    secret_key_project: str | None = None
    loglevel: str | None = None
    django_debug: str | None = None
    django_allowed_hosts: str | None = None
    env_path: Path = Path(__file__).resolve().parent.joinpath(".env")
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=env_path, env_file_encoding='utf-8'
    )


settings: Settings = Settings()
