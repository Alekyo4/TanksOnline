from tanksonline.actions import JsonRes
from tanksonline.models import (EventRef, Evt, MapModel, PlayerModel,
                                PlayerRef, Settings, Vector2)
from tanksonline.models.event import (MoveAimEvent, MoveEvent, PlayerExitEvent,
                                      PlayerJoinEvent)


class Room:
    def __init__(self, id: int, map: MapModel) -> None:
        self.id: int = id
        self.map: MapModel = map

        self.players: list[PlayerModel] = []

    async def broadcast(self, data: dict | EventRef, exclude: list[str] = []) -> None:
        for pl in self.players:
            if pl.room.control in exclude:
                continue

            try:
                await pl.ws.send_json(
                    JsonRes(data.dict() if isinstance(data, EventRef) else data)
                )
            except:
                pass

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

    # -- EVENT --

    async def _on_player_join(self, e: PlayerJoinEvent) -> None:
        await self.broadcast(
            EventRef(
                evt=Evt.PLAYER_JOIN.name, data={"name": e.name, "position": e.position}
            ),
            exclude=[e.control],
        )

    async def _on_player_exit(self, e: PlayerExitEvent) -> None:
        for pl in self.players:
            if pl.room.control == e.control:
                self.players.remove(pl)

                await self.broadcast(
                    EventRef(evt=Evt.PLAYER_EXIT.name, data={"name": pl.name})
                )

                break

    async def _on_move_aim(self, e: MoveAimEvent) -> None:
        player: PlayerModel | None = self.get_player(e.control)

        if not player:
            return

        await self.broadcast(
            EventRef(
                evt=Evt.MOVE_AIM.name,
                data={"name": player.name, "direction": e.direction},
            ),
            exclude=[e.control],
        )

    async def _on_move(self, e: MoveEvent) -> None:
        player: PlayerModel | None = self.get_player(e.control)

        if not player:
            return

        await self.broadcast(
            EventRef(
                evt=Evt.MOVE.name,
                data={
                    "name": player.name,
                    "rot": e.rot,
                    "position": e.position,
                },
            ),
            exclude=[e.control],
        )

    async def on(self, e: EventRef) -> None:
        n: str = e.evt.name.lower()  # type: ignore

        try:
            await getattr(self, f"_on_{n}")(e.data)
        except AttributeError:
            pass
