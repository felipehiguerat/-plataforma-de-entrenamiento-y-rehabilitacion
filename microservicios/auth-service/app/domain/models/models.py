# microservicios/auth-service/app/models.py

from typing import Optional, List
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Column
from pydantic import EmailStr
from sqlalchemy.dialects.postgresql import JSON

class User(SQLModel, table=True): 
   
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(unique=True, index=True, nullable=False)
    roles: List[str] = Field(default_factory=list, sa_column=Column(JSON))
    age: Optional[int] = None
    sex: Optional[str] = None
    objective: Optional[str] = None 
    email: EmailStr = Field(unique=True, index=True, nullable=False) 
    hashed_password: str = Field(nullable=False) 
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

