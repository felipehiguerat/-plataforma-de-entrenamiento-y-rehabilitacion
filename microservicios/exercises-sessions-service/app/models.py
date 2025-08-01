from sqlalchemy import Column, String, Integer, Float, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


from .database import Base

class ExerciseSession(Base):
    __tablename__ = "exercise_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    date = Column(Date, default=datetime.utcnow().date)  # Día de la sesión
    notes = Column(String, nullable=True)  # Día de la sesión
    

    exercises = relationship("Exercise", back_populates="session")


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("exercise_sessions.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    weight = Column(Float, nullable=True)
    reps = Column(Integer, nullable=True)
    series = Column(Integer, nullable=True)
    duration = Column(Float, nullable=True)
    distance = Column(Float, nullable=True)

    session = relationship("ExerciseSession", back_populates="exercises")
