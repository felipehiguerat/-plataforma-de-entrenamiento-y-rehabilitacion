from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from fastapi import Depends

from app.repository.bometric_repo import BiometricRepository
from app.servicies.biometric_service import BiometricService
from app.servicies.user_service import get_user_by_username


def get_db():
    """
    Función que crea y cierra la sesión de la base de datos automáticamente.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_biometric_repository() -> BiometricRepository:
    """
    Inyecta una instancia del repositorio de biometría.
    """
    return BiometricRepository()

def get_user_service() -> get_user_by_username:
    """
    Inyecta una instancia del cliente del microservicio de usuarios.
    """
    return get_user_by_username()

def get_biometric_service(
    biometric_repository: BiometricRepository = Depends(get_biometric_repository),
    user_service: get_user_by_username = Depends(get_user_service)
) -> BiometricService:
    """
    Inyecta una instancia del servicio de biometría.
    FastAPI se encarga automáticamente de proveer sus dependencias.
    """
    return BiometricService(
        biometric_repository=biometric_repository,
        user_service=user_service
    )