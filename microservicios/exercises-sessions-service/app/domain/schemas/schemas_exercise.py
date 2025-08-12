from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID



class ExerciseBase(BaseModel):
    pass


class ExerciseCreate(ExerciseBase):

    name_exercise: str=None
    name_session: str
    username: str
    description: Optional[str] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    series: Optional[int] = None
    duration: Optional[float] = None  
    distance: Optional[float] = None  
    


class ExerciseRead(ExerciseBase):
    session_id: UUID
    exercise_id: UUID
    name_exercise: str=None
    description: Optional[str] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    series: Optional[int] = None
    duration: Optional[float] = None  
    distance: Optional[float] = None   



    model_config = ConfigDict(from_attributes=True)

class ExerciseUpdate(ExerciseBase):
    name_exercise: str=None
    name_session: str
    username: str
    description: Optional[str] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    series: Optional[int] = None
    duration: Optional[float] = None  
    distance: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class ExerciseDelete(ExerciseBase):
    exercisename: str=None
    name_session: str
    username: str

    model_config = ConfigDict(from_attributes=True)