from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repository.crud_session import SessionRepository
from app.domain.schemas.schema_sesssion import (
    ExerciseSessionCreate, 
    ExerciseSessionRead, 
    ExerciseSessionDelete

)
from typing import List
from app.domain.schemas.schemas_exercise import ExerciseCreate, ExerciseRead
router = APIRouter(prefix="/sessions", tags=["Sessions"])


def get_session_repository(db: Session = Depends(get_db)):
    """Dependency to get a SessionRepository instance."""
    return SessionRepository(db)

# -------------------------
# Session endpoints
# -------------------------
@router.get("/by-username/{username}/sessions", response_model=List[ExerciseSessionRead])
async def get_sessions_by_username(
    username: str, 
    session_repo: SessionRepository = Depends(get_session_repository)
) -> List[ExerciseSessionRead]:
 
    return await session_repo.get_sessions_by_username(username)



@router.get("/", response_model=List[ExerciseSessionRead])
async def get_all_sessionset_all_sessions_with_usernames(
    session_repo: SessionRepository = Depends(get_session_repository)
):
   
    return await session_repo.get_all_sessions_with_usernames()

@router.post("/", response_model=ExerciseSessionRead, status_code=status.HTTP_201_CREATED)
async def create_session(
    session_data: ExerciseSessionCreate,
    session_repo: SessionRepository = Depends(get_session_repository)
):
    """Crea una nueva sesión de ejercicio a partir del nombre de usuario."""
    return await session_repo.create_session(session_data)


@router.delete("/", response_model=dict)
async def delete_session(
    session_data: ExerciseSessionDelete,
    session_repo: SessionRepository = Depends(get_session_repository)
):
    """
    Elimina una sesión por el nombre de usuario y el nombre de la sesión.
    """
    was_deleted = await session_repo.delete_session(session_data)
    
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session deleted successfully"}



