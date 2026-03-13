from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.websocket.connection_manager import manager
from app.utils.auth import decode_token
import json
from datetime import datetime

router = APIRouter(prefix="/ws", tags=["WebSocket"])

@router.websocket("/connect")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    Endpoint WebSocket para conexión en tiempo real.
    Requiere token JWT como parámetro de query.
    """
    # Validar token
    payload = decode_token(token)
    if payload is None:
        await websocket.close(code=4001, reason="Token inválido")
        return
    
    user_id = payload.get("user_id")
    
    # Conectar usuario
    await manager.connect(websocket, user_id)
    
    try:
        while True:
            # Recibir mensaje
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Procesar diferentes tipos de mensajes
            message_type = message.get("type")
            
            if message_type == "action":
                # Acción del usuario (ej: interacción en The Tester)
                action = message.get("action")
                username = message.get("username", f"Usuario {user_id}")
                action_data = message.get("data", {})
                
                await manager.broadcast_action(
                    action_type=action,
                    user_id=user_id,
                    username=username,
                    data=action_data
                )
            
            elif message_type == "message":
                # Mensaje directo
                recipient_id = message.get("recipient_id")
                content = message.get("content")
                
                if recipient_id:
                    # Mensaje privado
                    private_message = {
                        "type": "private_message",
                        "from_user_id": user_id,
                        "content": content,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    await manager.send_personal_message(recipient_id, private_message)
                else:
                    # Mensaje público
                    public_message = {
                        "type": "public_message",
                        "user_id": user_id,
                        "username": message.get("username", f"Usuario {user_id}"),
                        "content": content,
                        "timestamp": datetime.utcnow().isoformat()
                    }
                    await manager.broadcast_message(public_message)
            
            elif message_type == "heartbeat":
                # Mantener conexión viva
                await websocket.send_json({
                    "type": "heartbeat_ack",
                    "timestamp": datetime.utcnow().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        # Notificar que el usuario está offline
        await manager.broadcast_presence_update(user_id, "offline")
    
    except Exception as e:
        manager.disconnect(user_id)
        print(f"Error en WebSocket: {e}")

@router.get("/online-users", response_model=dict)
async def get_online_users():
    """Obtener lista de usuarios conectados."""
    users = manager.get_online_users()
    return {
        "success": True,
        "data": {
            "online_users": users,
            "total_connected": manager.get_user_count()
        }
    }
