# services/session_service.py

from sqlalchemy.orm import Session
from app.domain.models import ExerciseSession as SessionModel, Exercise
from app.domain.schemas.schema_sesssion import ExerciseSession
from app.domain.schemas.schemas_exercise import ExerciseCreate, ExerciseRead
from app.services.user_client import validate_user_exists,get_user_by_username

async def create_session(db: Session, session_data: ExerciseCreate) -> SessionModel:

    # Validamos si el usuario existe antes de crear la sesión
    await validate_user_exists(session_data.user_id)

    session = SessionModel(
        user_id=session_data.user_id,
        name_session=session_data.name_session  # Asegúrate de pasar el nombre
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    # Creamos los ejercicios asociados a la sesión
    for exercise_data in session_data.exercises:
        exercise = Exercise(
            name_exercise=exercise_data.name_exercise,
            description=exercise_data.description,
            weight=exercise_data.weight,
            reps=exercise_data.reps,
            series=exercise_data.series,
            duration=exercise_data.duration,
            distance=exercise_data.distance,
            session_id=session.id
        )
        db.add(exercise)

    db.commit()
    db.refresh(session)
    return session


## Funciones de lógica de negocio y búsqueda

async def get_session_by_username_and_name(db: Session, username: str, name_session: str) -> SessionModel | None:

    # 1. Obtener el user_id del otro servicio (auth-service)
    user_id = await get_user_by_username(username)
    
    if not user_id:
        return None
    user_id = user_id['id']
    # 2. Buscar la sesión en la base de datos local usando el user_id
    session = db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.name_session == name_session
    ).first()
    
    return session


async def add_exercise_to_session(db: Session, exercise_data: ExerciseCreate) -> Exercise:
  
    # Usar la función de servicio para encontrar la sesión correcta
    session = await get_session_by_username_and_name(db, exercise_data.username, exercise_data.name_session)

    if not session:
        raise ValueError("Session not found for the given user and session name.")
        
    # Crear la instancia del modelo Exercise, solo con los campos que pertenecen
    exercise = Exercise(
        name_exercise=exercise_data.name_exercise,
        description=exercise_data.description,
        weight=exercise_data.weight,
        reps=exercise_data.reps,
        series=exercise_data.series,
        duration=exercise_data.duration,
        distance=exercise_data.distance,
        session_id=session.id  # Asignamos el ID de la sesión encontrada
    )
    
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    
    return exercise


def get_sessions_by_user(db: Session, user_id: str) -> list[SessionModel]:

    return db.query(SessionModel).filter(SessionModel.user_id == user_id).all()

def get_session(db: Session, session_id: int) -> SessionModel | None:
   
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()

def delete_session(db: Session, session_id: int) -> SessionModel | None:
 
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
    return session