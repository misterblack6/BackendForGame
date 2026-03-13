import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración global de la aplicación."""
    
    # Base de datos
    DATABASE_URL: str = os.getenv("DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/prueba_humana")
    
    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30  # segundos
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
