from sqlalchemy.orm import Session
from app.domain.models.models import Exercise, ExerciseSession
from app.domain.schemas.schemas_exercise import ExerciseCreate, ExerciseRead
from app.domain.schemas.schema_sesssion import ExerciseSessionCreate, ExerciseSessionRead
# Importa los esquemas de sesión desde el archivo de sesiones

from typing import List, Optional
from app.services.user_client import  get_user_by_username, validate_user_exists




# ---------------------
# CRUD - Exercise
# ---------------------

def add_exercise_to_session(db: Session, exercise_data: ExerciseCreate) -> Exercise:
     if not exercise_data.session_id:
            raise ValueError("session_id is required for creating an exercise")
     exercise = Exercise(
     name=exercise_data.name,
     description=exercise_data.description,
     weight=exercise_data.weight,
     reps=exercise_data.reps,
     series=exercise_data.series,
     duration=exercise_data.duration,
     distance=exercise_data.distance,
     session_id=exercise_data.session_id
    )
     db.add(exercise)
     db.commit()
     db.refresh(exercise)
     return exercise


def get_all_exercises(db: Session) -> List[ExerciseRead]:
    return db.query(Exercise).all()


def get_exercises_by_session(db: Session, session_id: str) -> List[Exercise]:
    return db.query(Exercise).filter(Exercise.session_id == session_id).all()


def get_exercise(db: Session, exercise_id: str) -> Optional[Exercise]:
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()

async def get_exercises_by_username(db: Session, username: str) -> List[ExerciseRead]:
    user_data = await get_user_by_username(username)
    user_id = user_data["id"]
    sessions = db.query(ExerciseSession).filter(ExerciseSession.user_id == user_id).all()
    exercises = []
    for session in sessions:
        session_exercises = db.query(Exercise).filter(Exercise.session_id == session.id).all()
        for exercise in session_exercises:
            exercise_schema = ExerciseRead.model_validate(exercise)
            exercises.append(exercise_schema)
    return exercises


async def delete_exercise(db: Session, id: str):
    to_delete = db.query(Exercise).filter(Exercise.id == id).first()
    
    if to_delete:
        db.delete(to_delete)
        db.commit()
        return True
    
    return False