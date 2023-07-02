from random import randrange

from tanksonline.actions import JsonRes
from tanksonline.models import EventRef, Evt, MapModel, PlayerModel, PlayerRef
from tanksonline.models.event import (PlayerExitEvent, PlayerJoinEvent,
                                      PlayerMoveAimEvent, PlayerMoveEvent,
                                      PlayerShotEvent)
from tanksonline.models.inp import Vector2


class Room:
    def __init__(self, id: int, map: MapModel) -> None:
        self.id: int = id
        self.map: MapModel = map

        self.players: list[PlayerModel] = []

    async def send_json(self, player: PlayerModel, data: dict | EventRef) -> None:
        try:
            await player.ws.send_json(
                JsonRes(data.dict() if isinstance(data, EventRef) else data)
            )
        except:
            await self._on_player_exit(PlayerExitEvent(), player)

    async def broadcast(self, data: dict | EventRef, exclude: list[str] = []) -> None:
        for pl in self.players:
            if pl.room.control in exclude:
                continue

            await self.send_json(pl, data)

    def all_players(self, exclude: list[str] = []) -> list[PlayerRef]:
        pls_ref: list[PlayerRef] = []

        for pl in self.players:
            if not pl.room.control in exclude:
                pls_ref.append(PlayerRef(**pl.dict()))

        return pls_ref

    def get_player(self, control: str) -> PlayerModel | None:
        for pl in self.players:
            if control == pl.room.control:
                return pl

        return None

    # -- EVENTS --

    async def _on_player_dead(self, e: PlayerShotEvent, player: PlayerModel) -> None:
        data: PlayerJoinEvent = PlayerJoinEvent(
            name=player.name,
            position=Vector2(
                x=randrange(64, self.map.size.x - 64),
                y=randrange(64, self.map.size.y - 64),
            ),
        )

        await self.send_json(
            player,
            EventRef(evt=Evt.PLAYER_RESPAWN.name, data={**data.dict(exclude={"name"})}),
        )

        await self.broadcast(
            EventRef(evt=Evt.PLAYER_DEAD.name, data={"name": player.name}),
            exclude=[player.room.control],
        )

        await self._on_player_join(data, player)

    async def _on_player_shot(self, e: PlayerShotEvent, player: PlayerModel) -> None:
        await self.broadcast(
            EventRef(evt=Evt.PLAYER_SHOT.name, data={"name": player.name}),
            exclude=[player.room.control],
        )

    async def _on_player_join(self, e: PlayerJoinEvent, player: PlayerModel) -> None:
        await self.broadcast(
            EventRef(
                evt=Evt.PLAYER_JOIN.name, data={"name": e.name, "position": e.position}
            ),
            exclude=[player.room.control],
        )

    async def _on_player_exit(self, e: PlayerExitEvent, player: PlayerModel) -> None:
        self.players.remove(player)

        await self.broadcast(
            EventRef(evt=Evt.PLAYER_EXIT.name, data={"name": player.name})
        )

    async def _on_player_move_aim(
        self, e: PlayerMoveAimEvent, player: PlayerModel
    ) -> None:
        await self.broadcast(
            EventRef(
                evt=Evt.PLAYER_MOVE_AIM.name,
                data={"name": player.name, "direction": e.direction},
            ),
            exclude=[player.room.control],
        )

    async def _on_player_move(self, e: PlayerMoveEvent, player: PlayerModel) -> None:
        player.position = e.position

        await self.broadcast(
            EventRef(
                evt=Evt.PLAYER_MOVE.name,
                data={
                    "name": player.name,
                    "rot": e.rot,
                    "position": e.position,
                },
            ),
            exclude=[player.room.control],
        )

    async def on(self, e: EventRef) -> None:
        n: str = e.evt.name.lower()  # type: ignore

        try:
            try:
                await getattr(self, f"_on_{n}")(e.data, self.get_player(e.control))  # type: ignore
            except TypeError:
                await getattr(self, f"_on_{n}")(e.data)
        except AttributeError:
            pass
