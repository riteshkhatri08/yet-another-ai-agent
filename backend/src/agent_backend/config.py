from typing import Tuple, Type
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)
from pathlib import Path


# Define your settings model
class Settings(BaseSettings):
    host: str
    port: int
    username: str
    password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        yaml_file=Path(__file__).parent.parent / "resources" / "config.yaml",
    )

    # Customize the source order: env first, then YAML file
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            env_settings,  # environment variables have top priority
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            init_settings,
        )


# Instantiate settings: will load from .env (env vars) + config.yaml
settings = Settings()
