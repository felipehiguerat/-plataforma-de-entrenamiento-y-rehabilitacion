

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from app.database import create_db_and_tables, get_db
from app.models import User, UserCreate, UserLogin 
from app.security import verify_password, create_access_token, get_current_user_payload 
from app.crud import UserRepository
from app.models import User
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES 
from datetime import timedelta


app = FastAPI()


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

@app.on_event("startup")
def on_startup():
    create_db_and_tables() # Crea las tablas en la base de datos si no existen

@app.get("/")
async def read_root():
    return {"message": "Auth Service is running!"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.post("/users/", response_model=User)
def create_user(
    user: UserCreate,
    user_repo: UserRepository = Depends(get_user_repository)
):
    db_user = user_repo.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = user_repo.create_user(user) # Ahora esta función hashea la contraseña
    return new_user

# Tu ruta /users/ para obtener usuarios (para verificar)
@app.get("/users/", response_model=list[User])
def read_users(user_repo: UserRepository = Depends(get_user_repository)):
    users = user_repo.get_all_users()
    return users

# --- ¡Nueva ruta para el LOGIN! ---
@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    user_repo: UserRepository = Depends(get_user_repository)
):
    user = user_repo.get_user_by_email(form_data.username) 
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(
    user_repo: UserRepository = Depends(get_user_repository), # Inyectamos el repositorio
    token_payload: dict = Depends(get_current_user_payload) # Obtenemos el payload del token
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email: str = token_payload.get("sub")
    if email is None:
        raise credentials_exception

    user = user_repo.get_user_by_email(email)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")

    return user

@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user) 
):
    return current_user
