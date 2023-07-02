from pydantic import BaseModel, validator
from starlette.websockets import WebSocket

from tanksonline.models.inp import Vector2
from tanksonline.models.settings import inst as Settings


class PlayerInfRoom(BaseModel):
    room_id: int
    map_name: str
    control: str


class PlayerInf(BaseModel):
    name: str


class PlayerRef(BaseModel):
    name: str
    position: Vector2


class PlayerModel(BaseModel):
    room: PlayerInfRoom
    name: str
    position: Vector2
    ws: WebSocket

    @validator("name")
    def check_name(cls, value: str) -> str:
        assert (
            value.isascii()
            and Settings.room.name_min <= len(value) <= Settings.room.name_max
            and value.find(" ") == -1
        )

        return value

    class Config:
        arbitrary_types_allowed = True
