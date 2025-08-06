# app/api/dependencies.py

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from fastapi import Depends

from app.repository.bometric_repo import BiometricRepository
from app.servicies.biometric_service import BiometricService

def get_db():
    # ... (código para la sesión de base de datos)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_biometric_repository() -> BiometricRepository:
    return BiometricRepository()

def get_biometric_service(
    biometric_repository: BiometricRepository = Depends(get_biometric_repository)
) -> BiometricService:
    """
    Inyecta una instancia del servicio de biometría.
    """
    # Se crea el servicio pasando solo el repositorio, ya que el cliente de usuario
    # se importará directamente en el servicio.
    return BiometricService(
        biometric_repository=biometric_repository
    )