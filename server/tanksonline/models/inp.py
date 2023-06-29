from pydantic import BaseModel


class Vector2(BaseModel):
    x: int = 0
    y: int = 0
