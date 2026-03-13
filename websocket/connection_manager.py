from fastapi import WebSocket
from typing import List, Dict
from datetime import datetime
import json

class ConnectionManager:
    """Gestor de conexiones WebSocket."""
    
    def __init__(self):
        # Diccionario: user_id -> WebSocket
        self.active_connections: Dict[int, WebSocket] = {}
        # Diccionario: user_id -> información de presencia
        self.user_presence: Dict[int, dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: int):
        """Conectar usuario a WebSocket."""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.user_presence[user_id] = {
            "user_id": user_id,
            "status": "online",
            "connected_at": datetime.utcnow().isoformat()
        }
        
        # Notificar a otros usuarios que este usuario está online
        await self.broadcast_presence_update(user_id, "online")
    
    def disconnect(self, user_id: int):
        """Desconectar usuario."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        if user_id in self.user_presence:
            self.user_presence[user_id]["status"] = "offline"
            self.user_presence[user_id]["disconnected_at"] = datetime.utcnow().isoformat()
    
    async def broadcast_presence_update(self, user_id: int, status: str):
        """Difundir actualización de presencia."""
        message = {
            "type": "presence_update",
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        for conn_user_id, connection in self.active_connections.items():
            if conn_user_id != user_id:
                try:
                    await connection.send_json(message)
                except:
                    pass
    
    async def send_personal_message(self, user_id: int, message: dict):
        """Enviar mensaje a un usuario específico."""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
            except:
                self.disconnect(user_id)
    
    async def broadcast_message(self, message: dict, exclude_user_id: int = None):
        """Difundir mensaje a todos los usuarios conectados."""
        for user_id, connection in self.active_connections.items():
            if exclude_user_id and user_id == exclude_user_id:
                continue
            try:
                await connection.send_json(message)
            except:
                self.disconnect(user_id)
    
    async def broadcast_action(self, action_type: str, user_id: int, username: str, data: dict = None):
        """Difundir acción de usuario (ej: interacción en The Tester)."""
        message = {
            "type": "user_action",
            "action": action_type,
            "user_id": user_id,
            "username": username,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast_message(message, exclude_user_id=user_id)
    
    def get_online_users(self) -> List[dict]:
        """Obtener lista de usuarios conectados."""
        return [
            {
                "user_id": user_id,
                "status": self.user_presence[user_id]["status"],
                "connected_at": self.user_presence[user_id].get("connected_at")
            }
            for user_id in self.active_connections.keys()
        ]
    
    def get_user_count(self) -> int:
        """Obtener cantidad de usuarios conectados."""
        return len(self.active_connections)

# Instancia global
manager = ConnectionManager()
