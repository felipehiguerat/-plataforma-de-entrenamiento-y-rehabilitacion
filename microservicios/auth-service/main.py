
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session 
from app.database import create_db_and_tables, get_db 
from app.models import User, UserCreate 
from app.crud import UserRepository

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
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Verificar si el email ya existe (simplemente un ejemplo, la lógica real viene después)
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear el nuevo usuario (sin hashear la contraseña todavía)
    db_user = User(email=user.email, hashed_password=user.password) # Asignamos directamente la contraseña (temporal)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user # SQLModel permite devolver el objeto directamente

# Ejemplo de ruta para obtener usuarios (para verificar)
@app.get("/users/", response_model=list[User])
def read_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users