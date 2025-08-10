import asyncio
from typing import List, Optional
from uuid import UUID
import uuid
from app.services.user_client import get_user_by_username, validate_user_exists
from sqlmodel import Session, select
from app.domain.models.models import Exercise, ExerciseSession
from app.domain.schemas.schema_sesssion import (
    ExerciseSessionCreate, 
    ExerciseSessionRead,
    ExerciseSessionUpdate,
    ExerciseSessionDelete
)
from app.services.user_client import get_user_by_username, validate_user_exists
from fastapi import Depends, HTTPException

# ---------------------
# Repositorio de Sesiones de Ejercicio
# ---------------------

class SessionRepository:
    def __init__(self, db: Session):
        self.db = db

    async def create_session(self, session_data: ExerciseSessionCreate) -> ExerciseSessionRead:
    # 1. Obtener el user_id a partir del username
        user_data = await get_user_by_username(session_data.username)
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User with username '{session_data.username}' not found.")
    
        user_id = UUID(user_data["id"])

    # 2. Crear la sesión usando el user_id obtenido
        db_session = ExerciseSession(
        user_id=user_id,
        date=session_data.date,
        name_session=session_data.name_session
    )
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)

    # 3. Preparar la respuesta con el username
    # Corrección para Pydantic v2:
    # Primero crea el esquema de lectura, luego actualiza el campo 'username'
        response_schema = ExerciseSessionRead.model_validate(db_session)
        response_schema.username = session_data.username
    
        return response_schema
    

    async def get_all_sessions_with_usernames(self) -> List[ExerciseSessionRead]:
        sessions = self.db.exec(select(ExerciseSession)).all()
        
        if not sessions:
            return []

        tasks = [validate_user_exists(str(session.user_id)) for session in sessions]
        user_data_list = await asyncio.gather(*tasks)

        session_list = []
        for session, user_data in zip(sessions, user_data_list):
            username = user_data.get("username", "Unknown") if user_data else "Unknown"
            session_read = ExerciseSessionRead.model_validate(session)
            session_read.username = username
            session_list.append(session_read)

        return session_list
    
    

    async def get_sessions_by_username(self, username: str) -> List[ExerciseSessionRead]:
        # 1. Obtener datos del usuario
        user_data = await get_user_by_username(username)
        if not user_data:
            return []
    
        user_id = uuid.UUID(user_data["id"])
        
        sessions = self.db.exec(
            select(ExerciseSession).where(ExerciseSession.user_id == user_id)
        ).all()
     
        session_list = []
        for session in sessions:
            session_read = ExerciseSessionRead.model_validate(session)
            session_read.username = username
            session_list.append(session_read)            
        return session_list
    


    
    async def delete_session(self, session_data: ExerciseSessionDelete) -> bool:
        # 1. Obtener el user_id a partir del username
        user_data = await get_user_by_username(session_data.username)
        if not user_data:
            raise HTTPException(status_code=404, detail=f"User with username '{session_data.username}' not found.")
        
        user_id = uuid.UUID(user_data["id"])
        

        session_to_delete = self.db.exec(
            select(ExerciseSession).where(
                ExerciseSession.user_id == user_id,
                ExerciseSession.name_session == session_data.name_session
            )
        ).first()

        if not session_to_delete:
            raise HTTPException(status_code=404, detail="Session not found.")
        
        
        try:
            self.db.delete(session_to_delete)
            self.db.commit() # Confirma la transacción
            return True
        except Exception as e:
           
            self.db.rollback()
           
            print(f"Error al eliminar la sesión: {e}")
            return False 
       