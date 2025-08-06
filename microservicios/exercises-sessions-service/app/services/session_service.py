# services/session_service.py

from sqlalchemy.orm import Session
from app.domain.models import Session as SessionModel, Exercise
from app.domain.schemas.schemas_exercise import SessionCreate, ExerciseCreate
from user_client import validate_user_exists

async def create_session(db: Session, session_data: SessionCreate):
    # Validamos si el usuario existe antes de crear la sesión
    await validate_user_exists(session_data.user_id)

    session = SessionModel(user_id=session_data.user_id)

    db.add(session)
    db.commit()
    db.refresh(session)

    # Creamos los ejercicios asociados a la sesión
    for exercise_data in session_data.exercises:
        exercise = Exercise(
            name=exercise_data.name,
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

def get_sessions_by_user(db: Session, user_id: str):
    return db.query(SessionModel).filter(SessionModel.user_id == user_id).all()

def get_session(db: Session, session_id: int):
    return db.query(SessionModel).filter(SessionModel.id == session_id).first()

def delete_session(db: Session, session_id: int):
    session = db.query(SessionModel).filter(SessionModel.id == session_id).first()
    if session:
        db.delete(session)
        db.commit()
    return session
