from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from config import settings
from routers import auth, stats, websocket
from models.database import Base, engine
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crear tablas
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Backend Prueba Humana",
    description="API para el juego multijugador Prueba Humana",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(auth.router)
app.include_router(stats.router)
app.include_router(websocket.router)

# Rutas de salud
@app.get("/health", tags=["Sistema"])
async def health_check():
    """Verificar estado del servidor."""
    return {
        "status": "healthy",
        "service": "Backend Prueba Humana",
        "version": "1.0.0"
    }

@app.get("/", tags=["Sistema"])
async def root():
    """Raíz de la API."""
    return {
        "message": "Bienvenido al Backend de Prueba Humana",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "autenticación": "/auth",
            "estadísticas": "/stats",
            "websocket": "/ws/connect"
        }
    }

# Manejo de errores global
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Manejador global de excepciones."""
    logger.error(f"Error no manejado: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Error interno del servidor",
            "detail": str(exc) if settings.DEBUG else "Error interno"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
