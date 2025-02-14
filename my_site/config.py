"""
This module contains the configuration settings for the application.

It uses Pydantic to load environment variables from a .env file.
"""

from pathlib import Path
from typing import Annotated

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuration settings for the application.

    This class uses Pydantic to load environment variables from a specified
    .env file.
    """

    data_source_name: str | None = None
    secret_key_project: str | None = None
    loglevel: Annotated[str, Field(default="debug")]
    django_debug: Annotated[bool, Field(default=False)]
    django_allowed_hosts: Annotated[str, Field(default="localhost")]
    env_path: Path = Path(__file__).resolve().parent.parent.joinpath(".env")

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=env_path, env_file_encoding='utf-8'
    )


settings: Settings = Settings()
