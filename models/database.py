from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import enum
from app.config import settings

# Crear motor de base de datos
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelos de base de datos
class User(Base):
    """Modelo de usuario."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

class GameStat(Base):
    """Modelo de estadísticas de partida."""
    __tablename__ = "game_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    score = Column(Integer, nullable=False)
    difficulty = Column(Integer, nullable=False)  # 0-3
    time_taken = Column(Float, nullable=False)  # segundos
    test_type = Column(String(50), nullable=False)  # Nombre de la prueba
    weighted_score = Column(Float, nullable=False)  # Puntaje ponderado
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

class ActiveSession(Base):
    """Modelo de sesiones activas para presencia."""
    __tablename__ = "active_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    token = Column(String(500), unique=True, nullable=False)
    is_online = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)

# Crear tablas
Base.metadata.create_all(bind=engine)

def get_db():
    """Dependencia para obtener sesión de base de datos."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
