# Backend Prueba Humana

Backend 100% Python con FastAPI para el juego multijugador **Prueba Humana**, con autenticación JWT, estadísticas, leaderboards y comunicación en tiempo real vía WebSocket.

## 🚀 Características

✅ **Autenticación JWT** - Registro e inicio de sesión seguros  
✅ **API REST** - Endpoints para estadísticas y leaderboards  
✅ **WebSocket** - Comunicación en tiempo real  
✅ **Leaderboards** - Globales, por dificultad y por tipo de prueba  
✅ **Puntajes Ponderados** - Cálculo automático según dificultad  
✅ **Estadísticas Detalladas** - Análisis de rendimiento  
✅ **Documentación Completa** - Ejemplos en GDScript  

## 📋 Requisitos

- Python 3.8+
- MySQL 5.7+

## 🔧 Instalación

### 1. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o en Windows:
venv\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar base de datos

Ejecuta `SCHEMA.sql` en tu MySQL:

```bash
mysql -u root -p prueba_humana < SCHEMA.sql
```

### 4. Configurar variables de entorno

Crea `.env`:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/prueba_humana
SECRET_KEY=tu-clave-secreta-muy-segura
DEBUG=False
```

### 5. Ejecutar servidor

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Accede a `http://localhost:8000/docs` para documentación interactiva.

## 📁 Estructura

```
backend-prueba-humana/
├── models/              # Modelos SQLAlchemy
├── schemas/             # Esquemas Pydantic
├── routers/             # Endpoints REST y WebSocket
├── services/            # Lógica de negocio
├── utils/               # Autenticación y dependencias
├── websocket/           # Gestor de WebSocket
├── config.py            # Configuración
├── main.py              # Aplicación principal
├── requirements.txt     # Dependencias
├── SCHEMA.sql           # Esquema MySQL
└── README.md            # Este archivo
```

## 🔐 Endpoints Principales

### Autenticación
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Usuario actual
- `POST /auth/logout` - Cerrar sesión

### Estadísticas
- `POST /stats/register` - Registrar partida
- `GET /stats/user` - Estadísticas del usuario
- `GET /stats/leaderboard/global` - Leaderboard global
- `GET /stats/leaderboard/difficulty/{difficulty}` - Por dificultad
- `GET /stats/leaderboard/test/{test_type}` - Por tipo de prueba

### WebSocket
- `WS /ws/connect` - Conexión en tiempo real
- `GET /ws/online-users` - Usuarios conectados

## 🎮 Ejemplo en GDScript (Godot)

```gdscript
extends Node

const API_URL = "http://localhost:8000"
var access_token: String = ""

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

func _on_login_completed(result: int, response_code: int, headers: PackedStringArray, body: PackedByteArray) -> void:
    if response_code == 200:
        var response = JSON.parse_string(body.get_string_from_utf8())
        if response["success"]:
            access_token = response["data"]["access_token"]
            print("Login exitoso")
```

Ver `API_DOCUMENTATION.md` para más ejemplos.

## 📊 Multiplicadores de Dificultad

- Dificultad 0: 1.0x
- Dificultad 1: 1.3x
- Dificultad 2: 1.7x
- Dificultad 3: 2.2x

## 🔒 Seguridad

- Contraseñas encriptadas con bcrypt
- Tokens JWT con expiración configurable
- CORS configurable
- Validación con Pydantic

## 📝 Licencia

MIT

---

**Versión:** 1.0.0  
**Última actualización:** 13 de Marzo de 2026
