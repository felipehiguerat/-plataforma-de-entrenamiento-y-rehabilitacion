# microservicios/auth-service/app/models.py
from typing import Optional
from sqlmodel import Field, SQLModel 
from pydantic import EmailStr

class User(SQLModel, table=True): 
    id: Optional[int] = Field(default=None, primary_key=True) 
    email: EmailStr = Field(unique=True, index=True, nullable=False) 
    hashed_password: str = Field(nullable=False) 
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    # Aquí no necesitamos una clase Config para ORM_mode, SQLModel lo maneja automáticamente
    # No necesitamos schemas.py por separado para la salida básica, SQLModel ya es Pydantic

# Opcional: Si quieres un esquema de entrada más ligero (sin ID, solo email y password)
class UserCreate(SQLModel):
    email: EmailStr
    password: str

class UserLogin(SQLModel):
    email: EmailStr
    password: str