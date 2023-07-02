from enum import Enum
from typing import Any

from pydantic import BaseModel

from tanksonline.models.inp import Vector2


class PlayerRespawnEvent(BaseModel):
    pass


class PlayerDeadEvent(BaseModel):
    pass


class PlayerShotEvent(BaseModel):
    pass


class PlayerMoveAimEvent(BaseModel):
    direction: float


class PlayerMoveEvent(BaseModel):
    rot: float
    position: Vector2


class PlayerJoinEvent(BaseModel):
    name: str
    position: Vector2


class PlayerExitEvent(BaseModel):
    pass


class Evt(Enum):
    PLAYER_MOVE = PlayerMoveEvent
    PLAYER_MOVE_AIM = PlayerMoveAimEvent
    PLAYER_SHOT = PlayerShotEvent
    PLAYER_DEAD = PlayerDeadEvent
    PLAYER_RESPAWN = PlayerRespawnEvent
    PLAYER_JOIN = PlayerJoinEvent
    PLAYER_EXIT = PlayerExitEvent


class EventRef(BaseModel):
    evt: str | Evt
    control: str | None = None
    data: Any = {}
