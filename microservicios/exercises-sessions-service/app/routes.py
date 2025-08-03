from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud as crud_session
from app.schemas import (
    ExerciseSessionCreate, 
    ExerciseCreate, 
    ExerciseSessionRead, 
    ExerciseRead,
    ExerciseSessionDelete

)
from typing import List

router = APIRouter(prefix="/sessions", tags=["Sessions"])

# -------------------------
# Session endpoints
# -------------------------
@router.get("/by-username/{username}/sessions", response_model=List[ExerciseSessionRead])
async def get_sessions_by_username(username: str, db: Session = Depends(get_db)):
    return await crud_session.get_sessions_by_username(db, username)


@router.get("/by-username/{username}/exercises", response_model=List[ExerciseRead])
async def get_exercises_by_username(username: str, db: Session = Depends(get_db)):
    return await crud_session.get_exercises_by_username(db, username)


@router.get("/exercises", response_model=List[ExerciseRead])
def get_all_exercises(db: Session = Depends(get_db)):
    return crud_session.get_all_exercises(db)

@router.get("/user/{user_id}", response_model=List[ExerciseSessionRead])
async def get_sessions_by_user(user_id: str, db: Session = Depends(get_db)):
    return await crud_session.get_sessions_by_user(db, user_id)

@router.get("/{session_id}", response_model=ExerciseSessionRead)
async def get_session(session_id: str, db: Session = Depends(get_db)):
    return await crud_session.get_session(db, session_id)
   

@router.get("/", response_model=List[ExerciseSessionRead])
async def get_all_sessions(db: Session = Depends(get_db)):
    return await crud_session.get_all_sessions_with_usernames(db)

@router.post("/", response_model=ExerciseSessionCreate)
def create_session(session_data: ExerciseSessionCreate, db: Session = Depends(get_db)):
    return crud_session.create_session(db, session_data)


@router.delete("/{id}", response_model=ExerciseSessionDelete)
async def delete_session(id: str, db: Session = Depends(get_db)):
    was_deleted = await crud_session.delete_session(db=db, id=id)
    
    if not was_deleted:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return ExerciseSessionDelete(id=id)



# -------------------------
# Exercise endpoints
# -------------------------



@router.post("/exercises", response_model=ExerciseRead)
def add_exercise(exercise_data: ExerciseCreate, db: Session = Depends(get_db)):
    return crud_session.add_exercise_to_session(db, exercise_data)

@router.get("/exercises", response_model=List[ExerciseRead])
def get_all_exercises(db: Session = Depends(get_db)):
    return crud_session.get_all_exercises(db)

@router.get("/exercises/{exercise_id}", response_model=ExerciseRead)
def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = crud_session.get_exercise(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

@router.get("/{session_id}/exercises", response_model=List[ExerciseRead])
def get_exercises_by_session(session_id: str, db: Session = Depends(get_db)):
    return crud_session.get_exercises_by_session(db, session_id)


@router.delete("/exercise/{id}", response_model=dict)
async def delete_exercise(id: str, db: Session = Depends(get_db)):
    was_deleted = await crud_session.delete_exercise(db=db, id=id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail=" exercise not found")
    return {"message": "Exercise deleted successfully", "id": id}


