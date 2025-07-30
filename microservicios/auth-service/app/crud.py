from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select
from app.models import User, UserCreate, UserUpdate # Asegúrate que estos modelos están definidos en models.py

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user.username,       # Cambiado a minúsculas
            email=user.email,             # Cambiado a minúsculas
            hashed_password=hashed_password,
            age=user.age,                 # Cambiado a minúsculas
            sex=user.sex,                 # Cambiado a minúsculas
            objective=user.objective,     # Cambiado a minúsculas
            # is_active y is_admin tienen valores por defecto en el modelo User
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: str) -> Optional[User]:
        # Para UUID, puedes buscar por el ID de la tabla
        return self.db.get(User, UUID(user_id)) # Asegúrate de convertir a UUID

    def get_users(self, offset: int = 0, limit: int = 100) -> List[User]:
        statement = select(User).offset(offset).limit(limit)
        return self.db.exec(statement).all()

    def get_user_by_username(self, username: str) -> Optional[User]: # Cambiado a minúsculas
        statement = select(User).where(User.username == username) # Cambiado a minúsculas
        return self.db.exec(statement).first()

    def get_user_by_email(self, email: str) -> Optional[User]: # Añadida función para buscar por email
        statement = select(User).where(User.email == email) # Cambiado a minúsculas
        return self.db.exec(statement).first()

    def update_user(self, db_user: User) -> User:
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: str) -> None:
        user = self.db.get(User, UUID(user_id))
        if user:
            self.db.delete(user)
            self.db.commit()