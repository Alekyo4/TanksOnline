from typing import Any

from fastapi import APIRouter, WebSocket
from pydantic.error_wrappers import ValidationError
from starlette.websockets import WebSocketDisconnect
from websockets.exceptions import ConnectionClosedOK

from tanksonline.actions import JsonRes
from tanksonline.core.room import Room, RoomManager
from tanksonline.models import EventRef, Evt, PlayerInf, PlayerModel
from tanksonline.models.event import PlayerExitEvent

router: APIRouter = APIRouter()


@router.websocket_route("/")
async def room_connect(ws: WebSocket) -> None:
    await ws.accept()

    while True:
        try:
            player: PlayerModel = await RoomManager.join(
                PlayerInf(**(await ws.receive_json(mode="binary"))), ws=ws
            )
        except:
            try:
                await ws.send_json(
                    JsonRes("Player information is incorrect or invalid", status=False)
                )
            except:
                return

            continue

        break

    room: Room = RoomManager.get(player.room.room_id)

    try:
        await ws.send_json(
            JsonRes(
                {
                    "self": player.dict(exclude={"ws"}),
                    "players": [
                        x.dict()
                        for x in room.all_players(exclude=[player.room.control])
                    ],
                }
            )
        )
    except ConnectionClosedOK:
        return

    while True:
        try:
            try:
                e: EventRef = EventRef(**(await ws.receive_json(mode="binary")))
            except WebSocketDisconnect:
                await room.on(
                    EventRef(
                        evt=Evt.PLAYER_EXIT,
                        data=PlayerExitEvent(control=player.room.control),
                    )
                )

                if len(room.players) == 0:
                    RoomManager.delete(room.id)

                break

            try:
                ev: Evt = getattr(Evt, e.evt.upper())  # type: ignore
                evt: Any = ev.value(**e.data)

                await room.on(EventRef(evt=ev, data=evt))
            except AttributeError:
                raise TypeError

        except (ValidationError, TypeError):
            await ws.send_json(JsonRes("Nonexistent or invalid event", status=False))

            continue
