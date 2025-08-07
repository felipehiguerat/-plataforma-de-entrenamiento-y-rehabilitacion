from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta
from sqlmodel import Session

# Importaciones de tu microservicio
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.database import get_db
from app.security.security import get_password_hash, verify_password, create_access_token, get_current_user_payload
from app.domain.models.models import User
from app.domain.schemas.schemas import UserCreate, UserUpdate, Token, UserRead
from app.repository.crud import UserRepository



router = APIRouter(prefix="/users", tags=["Users"])


# ---------------------
# Dependencias
# ---------------------

def get_user_repository(db: Session = Depends(get_db)):
    """Dependencia para obtener el repositorio de usuarios."""
    return UserRepository(db)


# ---------------------
# Rutas de Autenticación
# ---------------------

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Ruta para autenticar un usuario y generar un token de acceso.
    """
    user = user_repo.get_user_by_username(form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# ---------------------
# Rutas de Usuarios
# ---------------------

@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Crea un nuevo usuario en la base de datos.
    """
    db_user_by_username = user_repo.get_user_by_username(user.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    db_user_by_email = user_repo.get_user_by_email(user.email)
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
            
    hashed_password = get_password_hash(user.password)
    new_user = user_repo.create_user(user, hashed_password)
    
    return new_user


@router.get("/", response_model=List[UserRead])
def read_users(
    offset: int = 0, 
    limit: int = 100, 
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Obtiene una lista paginada de todos los usuarios.
    """
    users = user_repo.get_users(offset=offset, limit=limit)
    return users


@router.get("/me/", response_model=UserRead)
async def read_users_me(
    current_user_payload: dict = Depends(get_current_user_payload),
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Obtiene los datos del usuario autenticado.
    """
    username = current_user_payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = user_repo.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user


@router.get("/{user_id}", response_model=UserRead)
def read_user_by_id(user_id: str, user_repo: UserRepository = Depends(get_user_repository)):
    """
    Obtiene los datos de un usuario por su ID.
    """
    user = user_repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/by-username/{username}", response_model=UserRead)
def read_user_by_username(username: str, user_repo: UserRepository = Depends(get_user_repository)):
    """
    Obtiene los datos de un usuario por su nombre de usuario.
    """
    user = user_repo.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/by-username/{username}", response_model=UserRead)
def update_user_by_username(
    username: str, 
    user: UserUpdate, 
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Actualiza los datos de un usuario por su nombre de usuario.
    """
    db_user = user_repo.get_user_by_username(username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    update_data = user.model_dump(exclude_unset=True) 
    
    if "password" in update_data:
        # La función get_password_hash ya está importada y lista para usarse
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    updated_user = user_repo.update_user(db_user, update_data)
    return updated_user


@router.delete("/by-username/{username}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_by_username(
    username: str, 
    user_repo: UserRepository = Depends(get_user_repository)
):
    """
    Elimina un usuario por su nombre de usuario.
    """
    user_to_delete = user_repo.get_user_by_username(username)
    if user_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # Llama al método del repositorio para eliminar el usuario
    user_repo.delete_user(user_to_delete)
    # Como el código de estado es 204, no es necesario retornar nada
    return {"detail": "User deleted successfully"}