from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select
from app.domain.models.models import Exercise, ExerciseSession
from app.domain.schemas.schema_sesssion import (
    ExerciseSessionCreate, 
    ExerciseSessionRead,
    ExerciseSessionUpdate
)
from app.services.user_client import get_user_by_username, validate_user_exists

# ---------------------
# Repositorio de Sesiones de Ejercicio
# ---------------------

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_session(self, session_data: ExerciseSessionCreate) -> ExerciseSession:
        db_session = ExerciseSession(
            user_id=session_data.user_id,
            date=session_data.date,
            name_session=session_data.name_session
        )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session
    
    async def get_sessions_by_user(self, user_id: UUID) -> List[ExerciseSessionRead]:
        sessions = self.db.exec(
            select(ExerciseSession).where(ExerciseSession.user_id == user_id)
        ).all()
        
        user_data = await validate_user_exists(str(user_id))
        username = user_data.get("username", "Unknown")
        
        return [
            ExerciseSessionRead.model_validate(session, update={'username': username}) 
            for session in sessions
        ]

    async def get_all_sessions_with_usernames(self) -> List[ExerciseSessionRead]:
        sessions = self.db.exec(select(ExerciseSession)).all()
        session_list = []
        for session in sessions:
            user_data = await validate_user_exists(str(session.user_id))
            username = user_data.get("username", "Unknown")
            session_list.append(
                ExerciseSessionRead.model_validate(session, update={'username': username})
            )
        return session_list
        
    async def get_session_by_id(self, session_id: UUID) -> Optional[ExerciseSessionRead]:
        session = self.db.get(ExerciseSession, session_id)
        if not session:
            return None
        
        user_data = await validate_user_exists(str(session.user_id))
        username = user_data.get("username", "Unknown")
        
        return ExerciseSessionRead.model_validate(session, update={'username': username})

    async def update_session(self, db_session: ExerciseSession, update_data: ExerciseSessionUpdate) -> ExerciseSession:
        session_data = update_data.model_dump(exclude_unset=True)
        for key, value in session_data.items():
            setattr(db_session, key, value)
        
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    async def delete_session(self, db_session: ExerciseSession) -> bool:
        # Eliminar ejercicios asociados antes de eliminar la sesión
        self.db.exec(
            select(Exercise).where(Exercise.session_id == db_session.id)
        ).delete()
        
        self.db.delete(db_session)
        self.db.commit()
        return True

    async def get_sessions_by_username(self, username: str) -> List[ExerciseSessionRead]:
        user_data = await get_user_by_username(username)
        if not user_data:
            return []
            
        user_id = user_data.get("id")
        sessions = self.db.exec(
            select(ExerciseSession).where(ExerciseSession.user_id == user_id)
        ).all()
        
        return [
            ExerciseSessionRead.model_validate(session, update={'username': username}) 
            for session in sessions
        ]