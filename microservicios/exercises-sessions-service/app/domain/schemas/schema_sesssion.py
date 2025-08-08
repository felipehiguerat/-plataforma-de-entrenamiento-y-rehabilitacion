from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from datetime import date
from uuid import UUID
from app.domain.models.models import Exercise, ExerciseSession
from app.domain.schemas.schemas_exercise import ExerciseRead




# ---------- Session Schemas ----------

class ExerciseSessionBase(BaseModel):
    date: date

class ExerciseSessionBased(BaseModel):
    pass
    
class ExerciseSessionCreate(ExerciseSessionBase):
    user_id: UUID
    name_session:str = None



class ExerciseSessionRead(ExerciseSessionBase):
    id: UUID
    user_id: UUID
    exercises: List[ExerciseRead] = []
    username: Optional[str] = None
    name: Optional[str] = None  

    model_config = ConfigDict(from_attributes=True)

class ExerciseSessionDelete(ExerciseSessionBased):
    id: UUID
    user_id: Optional[UUID] = None
    name_session: str = None


class ExerciseSessionUpdate(ExerciseSessionBase):
    name_session: Optional[str] = None
    