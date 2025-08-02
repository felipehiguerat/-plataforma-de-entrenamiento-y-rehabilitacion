from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud as crud_session
from app.schemas import (
    ExerciseSessionCreate, 
    ExerciseCreate, 
    ExerciseSessionRead, 
    ExerciseRead
)
from typing import List

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# -------------------------
# Session endpoints
# -------------------------

@router.post("/", response_model=ExerciseSessionCreate)
def create_session(session_data: ExerciseSessionCreate, db: Session = Depends(get_db)):
    return crud_session.create_session(db, session_data)

@router.get("/user/{user_id}", response_model=List[ExerciseSessionRead])
async def get_sessions_by_user(user_id: str, db: Session = Depends(get_db)):
    return await crud_session.get_sessions_by_user(db, user_id)

@router.get("/{session_id}", response_model=ExerciseSessionRead)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    return await crud_session.get_session(db, session_id)
   

@router.get("/", response_model=List[ExerciseSessionRead])
async def get_all_sessions(db: Session = Depends(get_db)):
    return await crud_session.get_all_sessions_with_usernames(db)


# -------------------------
# Exercise endpoints
# -------------------------

@router.post("/exercises", response_model=ExerciseRead)
def add_exercise(exercise_data: ExerciseCreate, db: Session = Depends(get_db)):
    return crud_session.add_exercise_to_session(db, exercise_data)

@router.get("/{session_id}/exercises", response_model=List[ExerciseRead])
def get_exercises_by_session(session_id: str, db: Session = Depends(get_db)):
    return crud_session.get_exercises_by_session(db, session_id)

@router.get("/exercises/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = crud_session.get_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise
