from sqlmodel import Session, select
from typing import Optional

from app.domain.models import User
from app.domain.schemas import UserCreate, UserLogin
from app.security.security import get_password_hash, verify_password

# -------------------------
# Funciones de utilidad
# -------------------------

def get_user_by_username_or_email(db: Session, username: str) -> Optional[User]:
    """
    Busca un usuario por su nombre de usuario o email.
    
    Esta función es útil para el proceso de inicio de sesión, ya que
    permite al usuario iniciar sesión con cualquiera de los dos campos.
    """
    # Usamos `select` de SQLModel para construir la consulta.
    statement = select(User).where(
        (User.username == username) | (User.email == username)
    )
    return db.exec(statement).first()

# -------------------------
# Servicios principales de Auth
# -------------------------

def create_new_user(db: Session, user_data: UserCreate) -> User:
    """
    Crea un nuevo usuario en la base de datos.
    
    Hashea la contraseña antes de guardarla para asegurar que no se almacene
    en texto plano.
    """
    # Hashea la contraseña proporcionada.
    hashed_password = get_password_hash(user_data.password)
    
    # Crea una nueva instancia del modelo `User` con los datos hasheados.
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        age=user_data.age,
        sex=user_data.sex,
        objective=user_data.objective
    )
    
    # Agrega el usuario a la base de datos, lo guarda y lo refresca.
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, user_login: UserLogin) -> Optional[User]:
    """
    Verifica las credenciales de un usuario.
    
    Busca al usuario por nombre o email y verifica si la contraseña
    proporcionada coincide con la hasheada en la base de datos.
    """
    # Intenta encontrar al usuario en la base de datos.
    user = get_user_by_username_or_email(db, user_login.username)
    
    # Si el usuario existe y la contraseña es correcta, devuelve el objeto `User`.
    if user and verify_password(user_login.password, user.hashed_password):
        return user
    
    # Si no se encuentra o las credenciales son incorrectas, devuelve None.
    return None