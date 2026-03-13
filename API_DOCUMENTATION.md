# Documentación de API - Backend Prueba Humana

## Introducción

Este documento describe todos los endpoints disponibles en el backend de **Prueba Humana**, un juego multijugador que requiere autenticación, gestión de estadísticas y comunicación en tiempo real.

---

## Tabla de Contenidos

1. [Autenticación](#autenticación)
2. [Estadísticas y Leaderboards](#estadísticas-y-leaderboards)
3. [WebSocket (Tiempo Real)](#websocket-tiempo-real)
4. [Códigos de Error](#códigos-de-error)
5. [Ejemplos en GDScript](#ejemplos-en-gdscript)

---

## Autenticación

### Registro de Usuario

**Endpoint:** `POST /auth/register`

**Descripción:** Registrar un nuevo usuario en el sistema.

**Body:**
```json
{
  "username": "jugador123",
  "password": "password123",
  "email": "jugador@example.com"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Usuario registrado exitosamente",
  "data": {
    "user": {
      "id": 1,
      "username": "jugador123",
      "email": "jugador@example.com"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

---

### Inicio de Sesión

**Endpoint:** `POST /auth/login`

**Descripción:** Iniciar sesión con usuario y contraseña.

**Body:**
```json
{
  "username": "jugador123",
  "password": "password123"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Sesión iniciada exitosamente",
  "data": {
    "user": {
      "id": 1,
      "username": "jugador123",
      "email": "jugador@example.com"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

---

### Obtener Usuario Actual

**Endpoint:** `GET /auth/me`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "username": "jugador123",
    "email": "jugador@example.com",
    "is_active": true,
    "created_at": "2026-03-13T14:30:00",
    "last_login": "2026-03-13T15:45:00"
  }
}
```

---

### Cerrar Sesión

**Endpoint:** `POST /auth/logout`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Sesión cerrada exitosamente"
}
```

---

## Estadísticas y Leaderboards

### Registrar Estadística de Partida

**Endpoint:** `POST /stats/register`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Body:**
```json
{
  "score": 8500,
  "difficulty": 2,
  "time_taken": 145.5,
  "test_type": "memory_test"
}
```

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "message": "Estadística registrada exitosamente",
  "data": {
    "id": 42,
    "score": 8500,
    "weighted_score": 14450.0,
    "difficulty": 2,
    "time_taken": 145.5,
    "test_type": "memory_test",
    "created_at": "2026-03-13T15:50:00"
  }
}
```

**Notas:**
- El `weighted_score` se calcula automáticamente multiplicando el score por el multiplicador de dificultad
- Multiplicadores: 0→1.0, 1→1.3, 2→1.7, 3→2.2

---

### Obtener Estadísticas del Usuario

**Endpoint:** `GET /stats/user`

**Headers:**
```
Authorization: Bearer {access_token}
```

**Query Parameters:**
- `user_id` (opcional): ID del usuario a consultar. Si no se proporciona, retorna las estadísticas del usuario actual.

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "data": {
    "user_id": 1,
    "username": "jugador123",
    "total_games": 15,
    "average_score": 7200.5,
    "best_score": 9500,
    "best_weighted_score": 20900.0,
    "total_time_played": 2145.75,
    "games_by_difficulty": {
      "0": 3,
      "1": 5,
      "2": 4,
      "3": 3
    },
    "games_by_test_type": {
      "memory_test": 7,
      "reaction_test": 5,
      "logic_test": 3
    },
    "recent_games": [
      {
        "id": 42,
        "score": 8500,
        "weighted_score": 14450.0,
        "difficulty": 2,
        "time_taken": 145.5,
        "test_type": "memory_test",
        "created_at": "2026-03-13T15:50:00"
      }
    ]
  }
}
```

---

### Leaderboard Global

**Endpoint:** `GET /stats/leaderboard/global`

**Query Parameters:**
- `page` (default: 1): Número de página
- `page_size` (default: 10, max: 100): Cantidad de resultados por página

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "data": {
    "entries": [
      {
        "rank": 1,
        "user_id": 5,
        "username": "top_player",
        "score": 9800,
        "weighted_score": 21560.0,
        "last_score_date": "2026-03-13T14:20:00"
      },
      {
        "rank": 2,
        "user_id": 1,
        "username": "jugador123",
        "score": 9500,
        "weighted_score": 20900.0,
        "last_score_date": "2026-03-13T15:50:00"
      }
    ],
    "total_entries": 42,
    "page": 1,
    "page_size": 10
  }
}
```

---

### Leaderboard por Dificultad

**Endpoint:** `GET /stats/leaderboard/difficulty/{difficulty}`

**Path Parameters:**
- `difficulty`: 0, 1, 2 o 3

**Query Parameters:**
- `page` (default: 1)
- `page_size` (default: 10, max: 100)

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "data": {
    "entries": [
      {
        "rank": 1,
        "user_id": 3,
        "username": "hard_mode_master",
        "score": 9200,
        "weighted_score": 20240.0,
        "difficulty": 3,
        "last_score_date": "2026-03-13T16:00:00"
      }
    ],
    "total_entries": 28,
    "page": 1,
    "page_size": 10
  }
}
```

---

### Leaderboard por Tipo de Prueba

**Endpoint:** `GET /stats/leaderboard/test/{test_type}`

**Path Parameters:**
- `test_type`: Nombre de la prueba (ej: "memory_test", "reaction_test")

**Query Parameters:**
- `page` (default: 1)
- `page_size` (default: 10, max: 100)

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "data": {
    "entries": [
      {
        "rank": 1,
        "user_id": 2,
        "username": "memory_champion",
        "score": 9600,
        "weighted_score": 16320.0,
        "test_type": "memory_test",
        "last_score_date": "2026-03-13T15:30:00"
      }
    ],
    "total_entries": 35,
    "page": 1,
    "page_size": 10
  }
}
```

---

## WebSocket (Tiempo Real)

### Conexión WebSocket

**Endpoint:** `WS /ws/connect?token={access_token}`

**Descripción:** Conectarse al servidor WebSocket para recibir mensajes y notificaciones en tiempo real.

**Autenticación:**
- Parámetro de query `token`: Token JWT obtenido en login

**Ejemplo de conexión:**
```
ws://localhost:8000/ws/connect?token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

### Tipos de Mensajes

#### 1. Acción del Usuario

**Enviar:**
```json
{
  "type": "action",
  "action": "code_activated",
  "username": "jugador123",
  "data": {
    "code": "MRBLACK",
    "reward": "Dark Theme"
  }
}
```

**Recibir (broadcast a otros usuarios):**
```json
{
  "type": "user_action",
  "action": "code_activated",
  "user_id": 1,
  "username": "jugador123",
  "data": {
    "code": "MRBLACK",
    "reward": "Dark Theme"
  },
  "timestamp": "2026-03-13T16:05:00"
}
```

---

#### 2. Mensaje Público

**Enviar:**
```json
{
  "type": "message",
  "username": "jugador123",
  "content": "¡Acabo de conseguir el mejor puntaje!"
}
```

**Recibir (broadcast a todos):**
```json
{
  "type": "public_message",
  "user_id": 1,
  "username": "jugador123",
  "content": "¡Acabo de conseguir el mejor puntaje!",
  "timestamp": "2026-03-13T16:05:30"
}
```

---

#### 3. Mensaje Privado

**Enviar:**
```json
{
  "type": "message",
  "recipient_id": 5,
  "content": "¡Hola! ¿Quieres jugar juntos?"
}
```

**Recibir (solo el destinatario):**
```json
{
  "type": "private_message",
  "from_user_id": 1,
  "content": "¡Hola! ¿Quieres jugar juntos?",
  "timestamp": "2026-03-13T16:05:45"
}
```

---

#### 4. Actualización de Presencia

**Recibir automáticamente cuando un usuario se conecta/desconecta:**
```json
{
  "type": "presence_update",
  "user_id": 3,
  "status": "online",
  "timestamp": "2026-03-13T16:06:00"
}
```

---

#### 5. Heartbeat (Mantener Conexión Viva)

**Enviar periódicamente (cada 30 segundos):**
```json
{
  "type": "heartbeat"
}
```

**Recibir:**
```json
{
  "type": "heartbeat_ack",
  "timestamp": "2026-03-13T16:06:15"
}
```

---

### Obtener Usuarios Conectados

**Endpoint:** `GET /ws/online-users`

**Respuesta Exitosa (200):**
```json
{
  "success": true,
  "data": {
    "online_users": [
      {
        "user_id": 1,
        "status": "online",
        "connected_at": "2026-03-13T16:00:00"
      },
      {
        "user_id": 3,
        "status": "online",
        "connected_at": "2026-03-13T16:02:30"
      }
    ],
    "total_connected": 2
  }
}
```

---

## Códigos de Error

| Código | Descripción |
|--------|-------------|
| 400 | Solicitud inválida (datos faltantes o inválidos) |
| 401 | No autorizado (token inválido o expirado) |
| 403 | Prohibido (usuario inactivo) |
| 404 | No encontrado (usuario o recurso no existe) |
| 500 | Error interno del servidor |

**Ejemplo de respuesta de error:**
```json
{
  "success": false,
  "error": "Usuario o contraseña incorrectos",
  "detail": "..."
}
```

---

## Ejemplos en GDScript

### 1. Registro e Inicio de Sesión

```gdscript
extends Node

const API_URL = "http://localhost:8000"
var http_client: HTTPClient
var access_token: String = ""

func register(username: String, password: String, email: String) -> void:
    var url = API_URL + "/auth/register"
    var body = JSON.stringify({
        "username": username,
        "password": password,
        "email": email
    })
    
    var headers = ["Content-Type: application/json"]
    var request = HTTPRequest.new()
    add_child(request)
    request.request_completed.connect(_on_register_completed)
    request.request(url, headers, HTTPClient.METHOD_POST, body)

func login(username: String, password: String) -> void:
    var url = API_URL + "/auth/login"
    var body = JSON.stringify({
        "username": username,
        "password": password
    })
    
    var headers = ["Content-Type: application/json"]
    var request = HTTPRequest.new()
    add_child(request)
    request.request_completed.connect(_on_login_completed)
    request.request(url, headers, HTTPClient.METHOD_POST, body)

func _on_register_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code == 200:
        var response = JSON.parse_string(body.get_string_from_utf8())
        if response["success"]:
            access_token = response["data"]["access_token"]
            print("Registro exitoso. Token: ", access_token)
    else:
        print("Error en registro: ", response_code)

func _on_login_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code == 200:
        var response = JSON.parse_string(body.get_string_from_utf8())
        if response["success"]:
            access_token = response["data"]["access_token"]
            print("Login exitoso. Token: ", access_token)
    else:
        print("Error en login: ", response_code)
```

---

### 2. Registrar Estadística de Partida

```gdscript
func register_game_stat(score: int, difficulty: int, time_taken: float, test_type: String) -> void:
    var url = API_URL + "/stats/register"
    var body = JSON.stringify({
        "score": score,
        "difficulty": difficulty,
        "time_taken": time_taken,
        "test_type": test_type
    })
    
    var headers = [
        "Content-Type: application/json",
        "Authorization: Bearer " + access_token
    ]
    
    var request = HTTPRequest.new()
    add_child(request)
    request.request_completed.connect(_on_stat_registered)
    request.request(url, headers, HTTPClient.METHOD_POST, body)

func _on_stat_registered(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code == 200:
        var response = JSON.parse_string(body.get_string_from_utf8())
        if response["success"]:
            print("Estadística registrada: ", response["data"])
    else:
        print("Error al registrar estadística: ", response_code)
```

---

### 3. Obtener Leaderboard Global

```gdscript
func get_leaderboard(page: int = 1, page_size: int = 10) -> void:
    var url = API_URL + "/stats/leaderboard/global?page=" + str(page) + "&page_size=" + str(page_size)
    
    var request = HTTPRequest.new()
    add_child(request)
    request.request_completed.connect(_on_leaderboard_received)
    request.request(url)

func _on_leaderboard_received(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code == 200:
        var response = JSON.parse_string(body.get_string_from_utf8())
        if response["success"]:
            var entries = response["data"]["entries"]
            for entry in entries:
                print(str(entry["rank"]) + ". " + entry["username"] + " - " + str(entry["weighted_score"]))
    else:
        print("Error al obtener leaderboard: ", response_code)
```

---

### 4. Conexión WebSocket

```gdscript
extends Node

const WS_URL = "ws://localhost:8000/ws/connect"
var websocket: WebSocketPeer
var access_token: String = ""

func connect_websocket() -> void:
    websocket = WebSocketPeer.new()
    var url = WS_URL + "?token=" + access_token
    websocket.connect_to_url(url)

func _process(delta: float) -> void:
    if websocket:
        websocket.poll()
        
        # Recibir mensajes
        while websocket.get_available_packet_count() > 0:
            var message = websocket.get_message()
            var data = JSON.parse_string(message.get_string_from_utf8())
            _handle_websocket_message(data)

func _handle_websocket_message(data: Dictionary) -> void:
    var message_type = data.get("type")
    
    match message_type:
        "user_action":
            print(data["username"] + " realizó acción: " + data["action"])
        "public_message":
            print(data["username"] + ": " + data["content"])
        "private_message":
            print("Mensaje privado de usuario " + str(data["from_user_id"]) + ": " + data["content"])
        "presence_update":
            print("Usuario " + str(data["user_id"]) + " está " + data["status"])
        "heartbeat_ack":
            print("Conexión activa")

func send_action(action: String, data: Dictionary = {}) -> void:
    if websocket and websocket.get_ready_state() == WebSocketPeer.STATE_OPEN:
        var message = JSON.stringify({
            "type": "action",
            "action": action,
            "username": "mi_usuario",
            "data": data
        })
        websocket.send_text(message)

func send_public_message(content: String) -> void:
    if websocket and websocket.get_ready_state() == WebSocketPeer.STATE_OPEN:
        var message = JSON.stringify({
            "type": "message",
            "username": "mi_usuario",
            "content": content
        })
        websocket.send_text(message)

func send_heartbeat() -> void:
    if websocket and websocket.get_ready_state() == WebSocketPeer.STATE_OPEN:
        var message = JSON.stringify({"type": "heartbeat"})
        websocket.send_text(message)
```

---

## Instalación y Despliegue

### Requisitos

- Python 3.8+
- MySQL 5.7+
- pip (gestor de paquetes de Python)

### Instalación Local

1. **Clonar el repositorio:**
```bash
git clone <repo-url>
cd prueba-humana-backend
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tu configuración de MySQL
```

5. **Ejecutar servidor:**
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Acceder a documentación interactiva:**
```
http://localhost:8000/docs
```

---

## Notas Importantes

- **Fallback Offline:** El cliente debe implementar almacenamiento local para estadísticas cuando no hay conexión a internet.
- **Tokens JWT:** Los tokens expiran después del tiempo configurado. Implementar refresh token en el cliente.
- **WebSocket Heartbeat:** Enviar heartbeat cada 30 segundos para mantener la conexión viva.
- **Rate Limiting:** Implementar en producción para evitar abuso.
- **HTTPS/WSS:** En producción, usar siempre HTTPS y WSS (WebSocket Seguro).

---

**Versión:** 1.0.0  
**Última actualización:** 13 de Marzo de 2026
