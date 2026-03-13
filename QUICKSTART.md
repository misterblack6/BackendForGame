# Guía de Inicio Rápido

## Instalación en 5 pasos

### 1. Descomprime el archivo

```bash
unzip backend-prueba-humana-CLEAN.zip
cd backend-prueba-humana
```

### 2. Crea el entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# o en Windows:
venv\Scripts\activate
```

### 3. Instala las dependencias

```bash
pip install -r requirements.txt
```

### 4. Configura la base de datos

Primero, crea la base de datos en MySQL:

```bash
mysql -u root -p < SCHEMA.sql
```

Luego, crea el archivo `.env`:

```bash
cat > .env << EOF
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/prueba_humana
SECRET_KEY=tu-clave-secreta-muy-segura
DEBUG=False
EOF
```

**Reemplaza `password` con tu contraseña de MySQL.**

### 5. Ejecuta el servidor

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Acceso

- **API Docs (Swagger):** http://localhost:8000/docs
- **API Docs (ReDoc):** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## Estructura del Proyecto

```
backend-prueba-humana/
├── config.py                 # Configuración global
├── main.py                   # Aplicación FastAPI
├── models/
│   └── database.py          # Modelos SQLAlchemy
├── schemas/
│   ├── user.py              # Esquemas de usuario
│   └── stats.py             # Esquemas de estadísticas
├── routers/
│   ├── auth.py              # Endpoints de autenticación
│   ├── stats.py             # Endpoints de estadísticas
│   └── websocket.py         # Endpoint WebSocket
├── services/
│   ├── auth_service.py      # Lógica de autenticación
│   └── stats_service.py     # Lógica de estadísticas
├── utils/
│   ├── auth.py              # Utilidades JWT
│   └── dependencies.py      # Dependencias FastAPI
├── websocket/
│   └── connection_manager.py # Gestor de conexiones
├── requirements.txt         # Dependencias Python
├── SCHEMA.sql               # Esquema MySQL
└── README.md                # Documentación completa
```

## Primeros Pasos

### 1. Registrar un usuario

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jugador1",
    "password": "password123",
    "email": "jugador1@example.com"
  }'
```

### 2. Iniciar sesión

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jugador1",
    "password": "password123"
  }'
```

Guarda el `access_token` de la respuesta.

### 3. Registrar una partida

```bash
curl -X POST "http://localhost:8000/stats/register" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {access_token}" \
  -d '{
    "score": 8500,
    "difficulty": 2,
    "time_taken": 145.5,
    "test_type": "memory_test"
  }'
```

### 4. Ver leaderboard global

```bash
curl "http://localhost:8000/stats/leaderboard/global?page=1&page_size=10"
```

## Solución de Problemas

### Error: "No module named 'fastapi'"

Asegúrate de haber activado el entorno virtual y ejecutado `pip install -r requirements.txt`.

### Error: "Can't connect to MySQL"

Verifica que:
1. MySQL está corriendo
2. La contraseña en `.env` es correcta
3. La base de datos `prueba_humana` existe

### Error: "Port 8000 already in use"

Usa otro puerto:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

## Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | Conexión MySQL | `mysql+pymysql://root:password@localhost:3306/prueba_humana` |
| `SECRET_KEY` | Clave para JWT | `your-secret-key-change-in-production` |
| `DEBUG` | Modo debug | `False` |
| `HOST` | Host del servidor | `0.0.0.0` |
| `PORT` | Puerto del servidor | `8000` |

## Documentación Completa

Ver `README.md` para documentación completa, ejemplos en GDScript y más detalles.

---

¡Listo! Tu backend está corriendo. 🚀
