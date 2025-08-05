from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.api.dependencies import get_db, get_biometric_service
from app.domain.schemas.schemas import (
    BiometricCreate,
    BiometricRead
    
)
from app.servicies.biometric_service import BiometricService

router = APIRouter(prefix="/biometrics", tags=["Biometrics"])


@router.post("/", response_model=BiometricRead, status_code=status.HTTP_201_CREATED)
def record_biometric_data(
    data: BiometricCreate,
    biometric_service: BiometricService = Depends(get_biometric_service),
    db: Session = Depends(get_db)
):
    """
    Crea un nuevo registro biométrico para un usuario.
    El IMC se calcula automáticamente.
    """
    return biometric_service.create_new_record(db, data)


@router.get("/user/{user_id}", response_model=List[BiometricRead])
def get_user_metrics_by_id(
    user_id: UUID,
    biometric_service: BiometricService = Depends(get_biometric_service),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los registros biométricos de un usuario por su ID.
    """
    records = biometric_service.get_biometric_data_by_user(db, user_id)
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron datos biométricos para el usuario con ID {user_id}",
        )
    return records


@router.get("/user/by_name/{user_name}", response_model=List[BiometricRead])
async def get_user_metrics_by_name(
    user_name: str,
    biometric_service: BiometricService = Depends(get_biometric_service),
    db: Session = Depends(get_db)
):
    """
    Obtiene todos los registros biométricos de un usuario por su nombre.
    """
    records = await biometric_service.get_by_user_name(db, user_name)
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron datos para el usuario con nombre {user_name}",
        )
    return records


@router.get("/analysis/user/{user_id}/type/{data_type}")
def get_user_progress_analysis(
    user_id: UUID,
    data_type: str,
    biometric_service: BiometricService = Depends(get_biometric_service),
    db: Session = Depends(get_db)
):
    """
    Provee un análisis de progreso para un tipo de dato biométrico específico.
    """
    analysis = biometric_service.analyze_progress(db, user_id, data_type)
    return analysis


@router.patch("/{biometric_id}", response_model=BiometricRead)
def update_biometric_record(
    biometric_id: UUID,
    biometric_update: BiometricCreate,
    biometric_service: BiometricService = Depends(get_biometric_service),
    db: Session = Depends(get_db)
):
    """
    Actualiza un registro biométrico existente por su ID.
    """
    updated_record = biometric_service.update_record(db, biometric_id, biometric_update)
    if not updated_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro biométrico con ID {biometric_id} no encontrado",
        )
    return updated_record


@router.delete("/{biometric_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_biometric_record(
    biometric_id: UUID,
    biometric_service: BiometricService = Depends(get_biometric_service),
    db: Session = Depends(get_db)
):
    """
    Elimina un registro biométrico por su ID.
    """
    was_deleted = biometric_service.delete_record(db, biometric_id)
    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Registro biométrico con ID {biometric_id} no encontrado",
        )
    return {"message": "Registro eliminado con éxito"}