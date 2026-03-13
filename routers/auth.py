from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from schemas.user import UserRegister, UserLogin
from services.auth_service import AuthService
from utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=dict)
async def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """Registrar nuevo usuario."""
    result = AuthService.register(db, user_data)
    return {
        "success": True,
        "message": "Usuario registrado exitosamente",
        "data": result
    }

@router.post("/login", response_model=dict)
async def login(
    user_data: UserLogin,
    db: Session = Depends(get_db)
):
    """Iniciar sesión de usuario."""
    result = AuthService.login(db, user_data)
    return {
        "success": True,
        "message": "Sesión iniciada exitosamente",
        "data": result
    }

@router.get("/me", response_model=dict)
async def get_current_user_info(
    current_user = Depends(get_current_user)
):
    """Obtener información del usuario actual."""
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "is_active": current_user.is_active,
            "created_at": current_user.created_at,
            "last_login": current_user.last_login
        }
    }

@router.post("/logout", response_model=dict)
async def logout(
    current_user = Depends(get_current_user)
):
    """Cerrar sesión de usuario."""
    return {
        "success": True,
        "message": "Sesión cerrada exitosamente"
    }
