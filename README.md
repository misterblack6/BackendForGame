# Backend Prueba Humana

Backend completo en Python/FastAPI para el juego multijugador **Prueba Humana**, con autenticación JWT, sistema de estadísticas, leaderboards y comunicación en tiempo real vía WebSocket.

## 🚀 Características

✅ **Autenticación JWT** - Registro e inicio de sesión seguros con tokens JWT  
✅ **API REST** - Endpoints para estadísticas, leaderboards y gestión de usuarios  
✅ **WebSocket** - Comunicación en tiempo real, mensajería y presencia  
✅ **Leaderboards** - Globales, por dificultad y por tipo de prueba  
✅ **Puntajes Ponderados** - Cálculo automático según multiplicadores de dificultad  
✅ **Estadísticas Detalladas** - Análisis de rendimiento del jugador  
✅ **Fallback Offline** - Soporte para modo offline en cliente  
✅ **Documentación Completa** - Ejemplos en GDScript para Godot  

## 📋 Requisitos

- Python 3.8 o superior
- MySQL 5.7 o superior
- pip (gestor de paquetes Python)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd prueba-humana-backend
```

### 2. Crear entorno virtual

```bash
# En Linux/macOS
python3 -m venv venv
source venv/bin/activate

# En Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar base de datos

Crear base de datos MySQL:

```sql
CREATE DATABASE prueba_humana CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tu configuración:

```env
DATABASE_URL=mysql+pymysql://usuario:contraseña@localhost:3306/prueba_humana
SECRET_KEY=tu-clave-secreta-muy-segura
DEBUG=False
```

### 6. Ejecutar servidor

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000`

## 📚 Documentación

### Acceder a documentación interactiva

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Documentación completa

Ver [`API_DOCUMENTATION.md`](./API_DOCUMENTATION.md) para:
- Descripción detallada de todos los endpoints
- Ejemplos de solicitudes y respuestas
- Ejemplos en GDScript para integración con Godot
- Guía de despliegue en producción

## 🎮 Integración con Godot

### Ejemplo básico de login

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

Ver más ejemplos en [`API_DOCUMENTATION.md`](./API_DOCUMENTATION.md#ejemplos-en-gdscript)

## 🏗️ Estructura del Proyecto

```
prueba-humana-backend/
├── app/
│   ├── models/           # Modelos SQLAlchemy
│   ├── schemas/          # Esquemas Pydantic
│   ├── routers/          # Rutas de la API
│   ├── services/         # Lógica de negocio
│   ├── utils/            # Utilidades (auth, dependencies)
│   ├── websocket/        # Gestión de WebSocket
│   ├── config.py         # Configuración
│   └── main.py           # Aplicación principal
├── requirements.txt      # Dependencias Python
├── .env.example          # Ejemplo de variables de entorno
├── API_DOCUMENTATION.md  # Documentación completa
└── README.md             # Este archivo
```

## 🔐 Seguridad

- **Contraseñas**: Encriptadas con bcrypt
- **Tokens JWT**: Expiración configurable
- **CORS**: Configurable según necesidad
- **Validación**: Todos los inputs validados con Pydantic

### Recomendaciones para Producción

1. Cambiar `SECRET_KEY` a una clave aleatoria fuerte
2. Usar HTTPS/WSS en lugar de HTTP/WS
3. Configurar CORS apropiadamente
4. Implementar rate limiting
5. Usar base de datos con contraseña fuerte
6. Habilitar SSL en MySQL
7. Configurar logs y monitoreo

## 📊 Endpoints Principales

### Autenticación
- `POST /auth/register` - Registrar usuario
- `POST /auth/login` - Iniciar sesión
- `GET /auth/me` - Obtener usuario actual
- `POST /auth/logout` - Cerrar sesión

### Estadísticas
- `POST /stats/register` - Registrar partida
- `GET /stats/user` - Obtener estadísticas del usuario
- `GET /stats/leaderboard/global` - Leaderboard global
- `GET /stats/leaderboard/difficulty/{difficulty}` - Leaderboard por dificultad
- `GET /stats/leaderboard/test/{test_type}` - Leaderboard por tipo de prueba

### WebSocket
- `WS /ws/connect` - Conexión WebSocket
- `GET /ws/online-users` - Usuarios conectados

## 🧪 Testing

Ejecutar tests:

```bash
pytest
```

## 📝 Licencia

MIT

## 👨‍💻 Autor

Backend creado para el juego **Prueba Humana**

## 📞 Soporte

Para reportar bugs o sugerencias, abrir un issue en el repositorio.

---

**Versión:** 1.0.0  
**Última actualización:** 13 de Marzo de 2026
