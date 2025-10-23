from typing import Tuple, Type, List, Any, Dict
import os
from functools import lru_cache
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
    PyprojectTomlConfigSettingsSource,
)
from pathlib import Path
from pydantic import BaseModel


# Define your settings model
class LLMSettings(BaseModel):
    host: str = "http://localhost:1234"
    model: str = "default"
    max_tokens: int = 512
    timeout_seconds: int = 120
    debug: bool = False


class Settings(BaseSettings):
    # Core server config
    host: str
    port: int
    username: str
    password: str

    # Service configurations
    llm: LLMSettings = LLMSettings()

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
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
        app_env = os.getenv("APP_ENV", "local").lower()
        resources_dir = Path(__file__).parent.parent / "resources"
        yaml_files: List[str] = [
            str(resources_dir / "config.yaml"),
            str(resources_dir / f"config.{app_env}.yaml"),
        ]
        yaml_source = YamlConfigSettingsSource(settings_cls, yaml_files)

        return (
            init_settings,  # explicit initialization overrides everything
            env_settings,
            dotenv_settings,
            yaml_source,
            file_secret_settings,
        )

@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Global cached settings instance
settings = get_settings()
