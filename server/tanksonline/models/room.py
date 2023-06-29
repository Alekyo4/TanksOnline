from pydantic import BaseModel

from tanksonline.models.inp import Vector2


class MapModel(BaseModel):
    name: str
    size: Vector2
