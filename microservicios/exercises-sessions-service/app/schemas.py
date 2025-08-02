from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID


# ---------- Exercise Schemas ----------

class ExerciseBase(BaseModel):
    name: str
    description: Optional[str] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    series: Optional[int] = None
    duration: Optional[float] = None  # en minutos, si aplica
    distance: Optional[float] = None  # en metros o km, si aplica


class ExerciseCreate(ExerciseBase):
    session_id: UUID  # ID de la sesión a la que pertenece


class ExerciseRead(ExerciseBase):
    id: UUID
    session_id: UUID
    seession_name: Optional[str] = None  



    model_config = ConfigDict(from_attributes=True)

# ---------- Session Schemas ----------

class ExerciseSessionBase(BaseModel):
    date: date


class ExerciseSessionCreate(ExerciseSessionBase):
    user_id: UUID
    name: Optional[str] = None



class ExerciseSessionRead(ExerciseSessionBase):
    id: UUID
    user_id: UUID
    exercises: List[ExerciseRead] = []
    username: Optional[str] = None
    name: Optional[str] = None  

    model_config = ConfigDict(from_attributes=True)
