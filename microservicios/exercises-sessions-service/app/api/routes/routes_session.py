from fastapi import APIRouter, Depends, HTTPException
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
async def get_sessions_by_username(username: str, db: Session = Depends(get_db)):
    return await SessionRepository.get_sessions_by_username(db, username)




@router.get("/user/{user_id}", response_model=List[ExerciseSessionRead])
async def get_sessions_by_user(user_id: str, db: Session = Depends(get_db)):
    return await SessionRepository.get_sessions_by_user(db, user_id)

@router.get("/{session_id}", response_model=ExerciseSessionRead)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    return await SessionRepository.get_session(db, session_id)
   

@router.get("/", response_model=List[ExerciseSessionRead])
async def get_all_sessions(db: Session = Depends(get_db)):
    return await SessionRepository.get_all_sessions_with_usernames(db)

@router.post("/", response_model=ExerciseSessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    session_data: ExerciseSessionCreate,
    session_repo: SessionRepository = Depends(get_session_repository)
):
    """Creates a new exercise session."""
    created_session = session_repo.create_session(session_data)
    return created_session


@router.delete("/{id}", response_model=ExerciseSessionDelete)
async def delete_session(id: str, db: Session = Depends(get_db)):
    was_deleted = await SessionRepository.delete_session(db=db, id=id)
    
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return ExerciseSessionDelete(id=id)



