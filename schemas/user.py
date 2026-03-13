from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class UserRegister(BaseModel):
    """Esquema para registro de usuario."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: Optional[EmailStr] = None

class UserLogin(BaseModel):
    """Esquema para inicio de sesión."""
    username: str
    password: str

class UserResponse(BaseModel):
    """Esquema de respuesta de usuario."""
    id: int
    username: str
    email: Optional[str]
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime]
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """Esquema de respuesta de token."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenPayload(BaseModel):
    """Payload del JWT."""
    sub: int  # user_id
    exp: int
    iat: int
