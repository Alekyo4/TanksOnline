from enum import Enum
from typing import Any

from pydantic import BaseModel

from tanksonline.models.inp import Vector2


class MoveAimEvent(BaseModel):
    control: str
    direction: float


class MoveEvent(BaseModel):
    control: str
    rot: Vector2
    position: Vector2


class PlayerJoinEvent(BaseModel):
    name: str
    control: str
    position: Vector2


class PlayerExitEvent(BaseModel):
    control: str


class Evt(Enum):
    MOVE = MoveEvent
    MOVE_AIM = MoveAimEvent
    PLAYER_JOIN = PlayerJoinEvent
    PLAYER_EXIT = PlayerExitEvent


class EventRef(BaseModel):
    evt: str | Evt
    data: Any
