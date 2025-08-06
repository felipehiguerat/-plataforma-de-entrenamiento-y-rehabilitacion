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
    
    imc = Column(Float, nullable=False)
    
    grasaCorporal = Column(Float, nullable=True)
    masaMuscular = Column(Float, nullable=True)
    
    # Se mantienen solo las nuevas columnas de presión arterial
    presionSistolica = Column(Integer, nullable=True)
    presionDiastolica = Column(Integer, nullable=True)
    
    frecuenciaCardiaca = Column(Integer, nullable=True)
    
    fechaRegistro = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Biometric(biometricId='{self.biometricId}', userId='{self.userId}')>"
