from fastapi import WebSocket
import logging


class ConnectionManager:
    log = logging.getLogger(__name__)

    def __init__(self):
        self.connections: list[WebSocket] = []
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.INFO)

    async def connect(self, websocket: WebSocket) -> None:
        self.log.info(f"Accepting connection {websocket}")
        await websocket.accept()
        self.connections.append(websocket)

    async def disconnect(self, websocket: WebSocket) -> None:
        await websocket.close()
        self.connections.remove(websocket)

    async def send(self, websocket: WebSocket, message: dict) -> None:
        await websocket.send(message)

    async def receive(self, websocket: WebSocket) -> dict:
        message = await websocket.receive()
        return message

    async def broadcast_message(self, message: dict) -> None:
        for connection in self.connections:
            await self.send(connection, message)


manager = ConnectionManager()
