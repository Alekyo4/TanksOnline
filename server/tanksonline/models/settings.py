from json import loads as loads_json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, BaseSettings


def json_maps(settings: BaseSettings) -> dict[str, Any]:
    enc: str | None = settings.__config__.env_file_encoding

    return loads_json(Path("maps.json").read_text(enc))


class RoomInfo(BaseModel):
    max: int


class Settings(BaseSettings):
    room: RoomInfo
    maps: list[dict]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

        env_nested_delimiter = "_"

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            return (init_settings, json_maps, env_settings, file_secret_settings)


inst: Settings = Settings()  # type: ignore
