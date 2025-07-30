# microservicios/auth-service/app/models.py

from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column
from pydantic import EmailStr
from sqlalchemy.dialects.postgresql import JSON

class User(SQLModel, table=True): 
    # id ya está en minúsculas, ¡excelente!
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    
    # ¡Cambiamos a minúsculas!
    username: str = Field(unique=True, index=True, nullable=False)
    roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    age: Optional[int] = None
    sex: Optional[str] = None
    objective: Optional[str] = None 
    email: EmailStr = Field(unique=True, index=True, nullable=False) 
    hashed_password: str = Field(nullable=False) 
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

class UserCreate(SQLModel):
    # ¡También en minúsculas aquí!
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    sex: Optional[str] = None
    objective: Optional[str] = None

class UserUpdate(SQLModel):
    # ¡Y aquí también!
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    roles: Optional[List[str]] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    objective: Optional[str] = None
    is_active: Optional[bool] = None
    is_admin: Optional[bool] = None
    
class UserLogin(SQLModel):
    # Y aquí
    username: str # Asumiendo que usarás username para el login estándar de OAuth2
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"