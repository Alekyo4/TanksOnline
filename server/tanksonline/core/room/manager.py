from random import choice, randrange
from uuid import uuid4

from fastapi import WebSocket

from tanksonline.core.room.room import Room
from tanksonline.models import (EventRef, Evt, MapModel, PlayerInf,
                                PlayerInfRoom, PlayerModel, Settings, Vector2)
from tanksonline.models.event import PlayerJoinEvent


class Manager:
    def __init__(self) -> None:
        self.rooms: list[Room] = []

    def get(self, id: int) -> Room:
        for room in self.rooms:
            if room.id == id:
                return room

        raise IndexError

    def create(self) -> Room:
        room: Room = Room(
            id=self.rooms[-1].id + 1 if len(self.rooms) > 0 else 0,
            map=MapModel(**choice(Settings.maps)),
        )

        self.rooms.append(room)

        return room

    def delete(self, id: int) -> None:
        for room in self.rooms:
            if room.id == id:
                self.rooms.remove(room)

            break

    async def join(self, pl: PlayerInf, ws: WebSocket) -> PlayerModel:
        room: Room | None = None

        for l_room in reversed(self.rooms):
            if len(l_room.players) == Settings.room.max:
                continue

            for pl_room in l_room.players:
                if pl.name == pl_room.name:
                    continue

            room = l_room

        if not room:
            room = self.create()

        player: PlayerModel = PlayerModel(
            room=PlayerInfRoom(
                room_id=room.id, control=str(uuid4()), map_name=room.map.name
            ),
            ws=ws,
            name=pl.name,
            position=Vector2(
                x=randrange(64, room.map.size.x - 64),
                y=randrange(64, room.map.size.y - 64),
            ),
        )

        room.players.append(player)

        await room.on(
            EventRef(
                evt=Evt.PLAYER_JOIN,
                data=PlayerJoinEvent(
                    name=player.name,
                    control=player.room.control,
                    position=player.position,
                ),
            )
        )

        return player


inst: Manager = Manager()
