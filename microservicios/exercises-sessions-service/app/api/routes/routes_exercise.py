from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.repository import  crud_exercise as crud_session
from app.domain.schemas.schemas_exercise import ExerciseCreate, ExerciseRead
from app.domain.schemas.schema_sesssion import ExerciseSessionCreate, ExerciseSessionRead




from typing import List

router = APIRouter(prefix="/sessions", tags=["Sessions"])


# -------------------------
# Exercise endpoints
# -------------------------



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



@router.get("/by-username/{username}/exercises", response_model=List[ExerciseRead])
async def get_exercises_by_username(username: str, db: Session = Depends(get_db)):
    return await crud_session.get_exercises_by_username(db, username)


@router.get("/exercises", response_model=List[ExerciseRead])
def get_all_exercises(db: Session = Depends(get_db)):
    return crud_session.get_all_exercises(db)



@router.post("/exercises", response_model=ExerciseRead, status_code=status.HTTP_201_CREATED)
async def create_new_exercise(exercise_data: ExerciseCreate, db: Session = Depends(get_db)):

    try:
       
        new_exercise = await crud_session.create_exercise(db, exercise_data)
        return new_exercise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/exercise/{id}", response_model=dict)
async def delete_exercise(id: str, db: Session = Depends(get_db)):
    was_deleted = await crud_session.delete_exercise(db=db, id=id)
    if not was_deleted:
        raise HTTPException(status_code=404, detail=" exercise not found")
    return {"message": "Exercise deleted successfully", "id": id}