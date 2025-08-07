from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select
from app.domain.models.models import User
from app.domain.schemas.schemas import UserCreate, UserUpdate
from app.security.security import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate, hashed_password: str) -> User:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            age=user.age,
            sex=user.sex,
            objective=user.objective,
            is_admin=False,
            is_active=True,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, user_id: UUID) -> Optional[User]:
        return self.db.get(User, user_id)

    def get_users(self, offset: int = 0, limit: int = 100) -> List[User]:
        statement = select(User).offset(offset).limit(limit)
        return self.db.exec(statement).all()

    def get_user_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self.db.exec(statement).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        statement = select(User).where(User.email == email)
        return self.db.exec(statement).first()

    def update_user(self, db_user: User, update_data: dict) -> User:
        # Usa .model_validate para actualizar solo los campos pasados en el dict
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, db_user: User) -> None:
        self.db.delete(db_user)
        self.db.commit()
