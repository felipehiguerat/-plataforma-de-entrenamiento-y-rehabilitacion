
from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column
from pydantic import EmailStr
from sqlalchemy.dialects.postgresql import JSON


class UserCreate(SQLModel):
   
    username: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    sex: Optional[str] = None
    objective: Optional[str] = None

class UserUpdate(SQLModel):
   
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



class UserRead(SQLModel):
    id: Optional[UUID]
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"