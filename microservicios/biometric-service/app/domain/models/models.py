import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Biometric(Base):
    __tablename__ = "biometric"
    
    biometricId = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    userId = Column(UUID(as_uuid=True), nullable=False)
    
    talla = Column(Float, nullable=False)
    peso = Column(Float, nullable=False)
    
    # IMC puede ser calculado en el servicio antes de guardar
    imc = Column(Float, nullable=False)
    
    grasaCorporal = Column(Float, nullable=True)
    masaMuscular = Column(Float, nullable=True)
    
    # Se separa la presión arterial para facilitar consultas
    presionSistolica = Column(Integer, nullable=True)
    presionDiastolica = Column(Integer, nullable=True)
    
    frecuenciaCardiaca = Column(Integer, nullable=True)
    
    # Se usa DateTime para el manejo correcto de fechas y horas
    fechaRegistro = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Biometric(biometricId='{self.biometricId}', userId='{self.userId}')>"

