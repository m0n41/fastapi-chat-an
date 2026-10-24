from fastapi import WebSocket, WebSocketDisconnect
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[WebSocket, dict] = {}
        
    def connect(self, websocket: WebSocket, username: str):
        self.active_connections[websocket] = username
        
    def disconnect(self, websocket: WebSocket) -> str | None:
        return self.active_connections.pop(websocket, None)
    
    async def broadcast(self, websocket: WebSocket | None, message: dict):
        dead: list[WebSocket] = []
        
        for connection in list(self.active_connections):
            if connection is websocket:
                continue
            
            try:
                await connection.send_json(message)
            except (WebSocketDisconnect, RuntimeError, OSError):
                logger.warning("Dropping dead connection %r", connection)
                dead.append(connection)
                
        for d in dead:
            self.disconnect(d)
            
manager = ConnectionManager()