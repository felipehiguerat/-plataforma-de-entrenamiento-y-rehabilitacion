
# microservicios/auth-service/app/crud.py
from typing import List, Optional
from sqlmodel import Session, select
from app.models import User, UserCreate
from app.security import get_password_hash

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su dirección de email."""
        # Usamos `select` de SQLModel para construir la consulta
        statement = select(User).where(User.email == email)
        return self.db.exec(statement).first()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su ID."""
        return self.db.get(User, user_id) # Método más directo para buscar por PK

    def get_all_users(self) -> List[User]:
        """Obtiene todos los usuarios."""
        statement = select(User)
        return self.db.exec(statement).all()

    def create_user(self, user_in: UserCreate) -> User:
        """Crea un nuevo usuario en la base de datos."""
        hashed_password = get_password_hash(user_in.password) 
        # Crea una instancia del modelo User a partir de UserCreate
        db_user = User(
            email=user_in.email,
            hashed_password=hashed_password, 
            is_active=True,
            is_admin=False
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user) 
        return db_user