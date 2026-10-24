from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.chat.connection_manager import manager

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        data = await websocket.receive_json()
    except WebSocketDisconnect:
        return
    
    username = (data.get("username") or "").strip()
    if not (2 <= len(username) <= 30):
        await websocket.close(code=1008)
        return
    
    manager.connect(websocket, username)
    await manager.broadcast(
        websocket,
        {"type": "system", "text": f"{username} подключился к чату"},
    )
    
    try:
        while True:
            data = await websocket.receive_json()
            text = (data.get("text") or "").strip()
            if not (1 <= len(text) <= 1000):
                await websocket.send_json({
                    "type": "error",
                    "detail": "Invalid message format",
                })
                continue
            await manager.broadcast(None, {
                "type": "message",
                "username": username,
                "text": text,
            })
    except WebSocketDisconnect:
        pass
    finally:
        username = manager.disconnect(websocket)
        if username:
            await manager.broadcast(
                None,
                {"type": "system", "text": f"{username} отключился от чата"},
            )
        await manager.broadcast(
            None,
            {"type": "system", "text": f"Аноним отключился от чата"},
        )