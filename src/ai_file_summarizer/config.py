import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str
    model: str


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ConfigError(f"Missing {name} in .env")
    return value


def get_settings() -> Settings:
    return Settings(
        api_key=_require("LLM_API_KEY"),
        base_url=_require("LLM_BASE_URL"),
        model=_require("LLM_MODEL"),
    )