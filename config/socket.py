from typing import Dict

from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] =websocket

    def disconnect(self, user_id: int):
        del self.active_connections[user_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def send_to_user(self, message, user_id: int):
        print(message)
        for id,connection in self.active_connections.items():
            if id == user_id:
                await connection.send_json(message)
                return True
        return False

    async def broadcast(self, message: str):
        for _,connection in self.active_connections.items():
            await connection.send_text(message)

manager: ConnectionManager = ConnectionManager()

