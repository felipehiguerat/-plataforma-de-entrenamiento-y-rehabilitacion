# microservicios/auth-service/app/main.py

from datetime import timedelta
from typing import List, Optional
from uuid import UUID # Necesario si user_id es UUID

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session # Usamos Session de sqlmodel, no sqlalchemy.orm.Session directamente
from fastapi.middleware.cors import CORSMiddleware

# Importaciones de tus módulos externos (asumiendo sus rutas y contenidos)
from app.database import create_db_and_tables, get_db # Corregido: get_db en lugar de get_session
from app.models import User, UserCreate, UserLogin, UserUpdate,Token # Asegúrate de que Token esté definido en models.py
from app.crud import UserRepository
from app.security import verify_password, create_access_token, get_current_user_payload, oauth2_scheme,get_password_hash # Asumiendo estas funciones en security.py
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES # Asumiendo ACCESS_TOKEN_EXPIRE_MINUTES viene de config.py


app = FastAPI(
    title="Auth Service API",
    version="0.1.0",
    description="API for user authentication and management"
)

# Configuración CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://127.0.0.1",
    "http://127.0.0.1:8002"
    # Añade más orígenes si tu frontend corre en otro puerto/dominio
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Permite todas las cabeceras
)

# --- Dependencias ---
# Helper para obtener una instancia de UserRepository con una sesión de DB
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

# --- Eventos de la Aplicación ---
@app.on_event("startup")
def on_startup():
    print("Creating Auth Service database tables...")
    create_db_and_tables()

# --- Rutas de Salud y Raíz ---
@app.get("/")
async def read_root():
    return {"message": "Auth Service is running!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# --- Rutas de Usuario (User Endpoints) ---

@app.post("/users/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate, 
    user_repo: UserRepository = Depends(get_user_repository) # Usamos la dependencia del repositorio
):
    # Verificar si el username ya existe (ahora en minúsculas)
    db_user_by_username = user_repo.get_user_by_username(user.username)
    if db_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verificar si el email ya existe (ahora en minúsculas)
    db_user_by_email = user_repo.get_user_by_email(user.email) # Asegúrate que esta función exista en crud.py
    if db_user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
            
    # Hashear la contraseña (ahora en minúsculas)
    hashed_password = get_password_hash(user.password) # Asumiendo get_password_hash viene de app.security
    
    # Crear el nuevo usuario usando el repositorio (todos los campos en minúsculas)
    new_user = user_repo.create_user(user, hashed_password)
    
    return new_user

@app.get("/users/", response_model=List[User])
def read_users(
    offset: int = 0, limit: int = 100, user_repo: UserRepository = Depends(get_user_repository)
):
    users = user_repo.get_users(offset=offset, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: str, user_repo: UserRepository = Depends(get_user_repository)): # user_id es string para UUID
    user = user_repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.patch("/users/{user_id}", response_model=User)
def update_user(user_id: str, user: UserUpdate, user_repo: UserRepository = Depends(get_user_repository)):
    db_user = user_repo.get_user(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Actualizar campos (ahora en minúsculas)
    # .model_dump() con exclude_unset=True evita que los campos no proporcionados se actualicen a None
    update_data = user.model_dump(exclude_unset=True) 
    
    if "password" in update_data: # Si se está actualizando la contraseña, hashearla
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    # Aplicar actualizaciones al modelo existente
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db_user = user_repo.update_user(db_user)
    return db_user

@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: str, user_repo: UserRepository = Depends(get_user_repository)):
    user = user_repo.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_repo.delete_user(user_id)
    return user

# --- Rutas de Autenticación (Authentication Endpoints) ---

@app.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    user_repo: UserRepository = Depends(get_user_repository)
):
    # OAuth2PasswordRequestForm usa 'username' y 'password' por defecto
    user = user_repo.get_user_by_username(form_data.username)
    
    # Verificar contraseña (ahora con user.hashed_password)
    if not user or not verify_password(form_data.password, user.hashed_password): # Asumiendo verify_password viene de app.security
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token de acceso (ahora con user.username)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token( # Asumiendo create_access_token viene de app.security
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Ruta para el usuario actual (requiere token JWT)
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user_payload: dict = Depends(get_current_user_payload),
    user_repo: UserRepository = Depends(get_user_repository)
):
    # Asegúrate de que get_current_user_payload (o la función asociada a oauth2_scheme)
    # te devuelva el payload decodificado del token.
    # Luego, usa el 'sub' (username) para obtener el objeto User completo de la base de datos.
    username = current_user_payload.get("sub")
    if not username:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
    user = user_repo.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

@app.get("/users/by-username/{username}", response_model=User)
def read_user_by_username(username: str, user_repo: UserRepository = Depends(get_user_repository)):
    user = user_repo.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user