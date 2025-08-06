from sqlalchemy.orm import Session
from app.domain.models import Exercise, ExerciseSession
from app.domain.schemas.schema_sesssion import ExerciseCreate, ExerciseSessionCreate, ExerciseSessionRead, ExerciseRead
from typing import List, Optional
from app.services.user_client import  get_user_by_username, validate_user_exists


# ---------------------
# CRUD - ExerciseSession
# ---------------------

def create_session(db: Session, session_data: ExerciseSessionCreate) -> ExerciseSession:
    session = ExerciseSession(
        user_id=session_data.user_id,
        date=session_data.date,
        name=session_data.name
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


async def get_sessions_by_user(db: Session, user_id: str) -> List[ExerciseSessionRead]:
    sessions = db.query(ExerciseSession).filter(ExerciseSession.user_id == user_id).all()
    user_data = await validate_user_exists(user_id)
    username = user_data.get("username", "Unknown")
    name = user_data.get("name", "Unknown")

    session_list = []
    for session in sessions:
        session_schema = ExerciseSessionRead.model_validate(session)
        session_schema.username = username
        session_list.append(session_schema)

    return session_list

async def get_all_sessions_with_usernames(db: Session) -> List[ExerciseSessionRead]:
    sessions = db.query(ExerciseSession).all()
    session_list = []
    for session in sessions:
        user_data = await validate_user_exists(str(session.user_id))
        username = user_data.get("username", "Unknown")
        name = user_data.get("name", "Unknown")
        session_schema = ExerciseSessionRead.model_validate(session)
        session_schema.username = username
        session_list.append(session_schema)
    return session_list


async def get_session(db: Session, id: str) -> ExerciseSessionRead:
    # 1. Obtener una sola sesión de la base de datos
    session = db.query(ExerciseSession).filter(ExerciseSession.id == id).first()
    
    # 2. Manejar el caso en que la sesión no se encuentre
    if not session:
        return None # O lanzar una excepción HTTP 404
    
    user_data = await validate_user_exists(session.user_id)
    username = user_data.get("username", "Unknown")
    session_schema = ExerciseSessionRead.model_validate(session)
    session_schema.username = username

    return session_schema

async def delete_session(db: Session, id: str):
    
    db.query(Exercise).filter(Exercise.session_id == id).delete()
    
    to_delete = db.query(ExerciseSession).filter(ExerciseSession.id == id).first()
    if to_delete:
        db.delete(to_delete)
        db.commit()
        return True
    return False


async def get_sessions_by_username(db: Session, username: str) -> List[ExerciseSessionRead]:
    user_data = await get_user_by_username(username)
    user_id = user_data["id"]
    sessions = db.query(ExerciseSession).filter(ExerciseSession.user_id == user_id).all()
    session_list = []
    for session in sessions:
        session_schema = ExerciseSessionRead.model_validate(session)
        session_schema.username = username
        session_list.append(session_schema)
    return session_list

