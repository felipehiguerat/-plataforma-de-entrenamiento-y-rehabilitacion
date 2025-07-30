# microservicios/exercises-sessions-service/app/main.py
from contextlib import asynccontextmanager
from typing import Optional, List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Field, Session, SQLModel, create_engine, select
from app.config import settings

# --- Modelos de la Base de Datos ---

class Exercise(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    series:int
    repeticiones:int
    description: Optional[str] = None
    # Puedes agregar otros campos relevantes para un ejercicio
    # Ejemplo: owner_id: int = Field(foreign_key="user.id") si tuvieras un servicio de usuarios centralizado

class SessionRecord(SQLModel, table=True): # Renombrado para evitar conflicto con sqlmodel.Session
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int # Clave foránea al usuario, para asociar la sesión a un usuario
    date: str # Considera usar datetime.date o datetime.datetime
    duration_minutes: int
    notes: Optional[str] = None
    # Agrega otros campos relevantes para una sesión, como qué ejercicios se hicieron

# --- Configuración de la Base de Datos ---
# La URL de la base de datos se toma de app/config.py, que a su vez la obtiene de las variables de entorno de Docker Compose
engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables():
    # Crea las tablas definidas por SQLModel en la base de datos conectada al engine
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating exercises and sessions tables...")
    create_db_and_tables()
    yield
    print("Shutting down exercises and sessions service...")

# Instancia principal de FastAPI para este microservicio
app = FastAPI(lifespan=lifespan)

# --- Endpoints (rutas API) ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Exercises & Sessions Service!"}

# Endpoint para crear un ejercicio
@app.post("/exercises/", response_model=Exercise, status_code=status.HTTP_201_CREATED)
def create_exercise(exercise: Exercise):
    print(f"DEBUG: Exercise object received: {exercise.model_dump()}") 
    with Session(engine) as session:
        session.add(exercise)
        session.commit()
        session.refresh(exercise)
        return exercise

# Endpoint para obtener todos los ejercicios
@app.get("/exercises/", response_model=List[Exercise])
def read_exercises():
    with Session(engine) as session:
        exercises = session.exec(select(Exercise)).all()
        return exercises

# Endpoint para crear un registro de sesión (ejemplo)
@app.post("/sessions/", response_model=SessionRecord, status_code=status.HTTP_201_CREATED)
def create_session_record(session_record: SessionRecord):
    with Session(engine) as session:
        session.add(session_record)
        session.commit()
        session.refresh(session_record)
        return session_record

# Endpoint para obtener todos los registros de sesiones (ejemplo)
@app.get("/sessions/", response_model=List[SessionRecord])
def read_session_records():
    with Session(engine) as session:
        session_records = session.exec(select(SessionRecord)).all()
        return session_records

# NOTA: Aquí es donde integrarías la seguridad (JWT)
# Por ejemplo, para proteger las rutas, necesitarías un Depends(oauth2_scheme)
# y lógica para verificar el token del auth-service.