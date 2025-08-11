from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID



class ExerciseBase(BaseModel):
    pass


class ExerciseCreate(ExerciseBase):

    exercise_name: str=None
    session_name: str
    user_name: str
    description: Optional[str] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    series: Optional[int] = None
    duration: Optional[float] = None  
    distance: Optional[float] = None  
    


class ExerciseRead(ExerciseBase):
    session_id: UUID
    user_id: UUID
    exercise_id: UUID
    exercise_name: str=None
    session_name: str
    user_name: str
    description: Optional[str] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    series: Optional[int] = None
    duration: Optional[float] = None  
    distance: Optional[float] = None   



    model_config = ConfigDict(from_attributes=True)

class ExerciseUpdate(ExerciseBase):
    exercise_name: str=None
    session_name: str
    user_name: str
    description: Optional[str] = None
    weight: Optional[float] = None
    reps: Optional[int] = None
    series: Optional[int] = None
    duration: Optional[float] = None  
    distance: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class ExerciseDelete(ExerciseBase):
    exercisename: str=None
    session_name: str
    user_name: str

    model_config = ConfigDict(from_attributes=True)