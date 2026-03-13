from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.database import User
from app.utils.auth import hash_password, verify_password, create_access_token, create_refresh_token
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from datetime import datetime
from fastapi import HTTPException, status

class AuthService:
    """Servicio de autenticación."""
    
    @staticmethod
    def register(db: Session, user_data: UserRegister) -> dict:
        """Registrar nuevo usuario."""
        # Verificar si el usuario ya existe
        existing_user = db.query(User).filter(
            (User.username == user_data.username) | 
            (User.email == user_data.email)
        ).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario o email ya existe"
            )
        
        # Crear nuevo usuario
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Generar tokens
        access_token = create_access_token(new_user.id)
        refresh_token = create_refresh_token(new_user.id)
        
        return {
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def login(db: Session, user_data: UserLogin) -> dict:
        """Iniciar sesión de usuario."""
        # Buscar usuario
        user = db.query(User).filter(User.username == user_data.username).first()
        
        if not user or not verify_password(user_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        # Actualizar último login
        user.last_login = datetime.utcnow()
        db.commit()
        
        # Generar tokens
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)
        
        return {
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            },
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Obtener usuario por ID."""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return user
