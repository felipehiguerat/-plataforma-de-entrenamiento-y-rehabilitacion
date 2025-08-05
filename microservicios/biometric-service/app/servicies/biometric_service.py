# app/services/biometric_service.py
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Dict, Any
from datetime import datetime, timedelta


from app.domain.schemas.schemas import BiometricRead,BiometricBase,BiometricCreate
from app.repository.bometric_repo import BiometricRepository

class BiometricService:
    def __init__(self, biometric_repository: BiometricRepository):
        self.biometric_repository = biometric_repository

    def create_biometric_data(self, db: Session, data: BiometricCreate) -> BiometricRead:
        """
        Crea un nuevo registro biométrico.
        La lógica del IMC se maneja automáticamente en el esquema de Pydantic.
        """
        return self.biometric_repository.create(db, data)

    def get_biometric_data_by_user(self, db: Session, user_id: UUID) -> List[BiometricRead]:
        """
        Obtiene todos los registros biométricos de un usuario.
        """
        return self.biometric_repository.get_by_user_id(db, user_id)

    def analyze_progress(self, db: Session, user_id: UUID, data_type: str) -> Dict[str, Any]:
        """
        Analiza el progreso de un usuario para una métrica específica.
        Esta es la lógica de negocio que va más allá de un simple CRUD.
        """
        # 1. Obtener los datos del repositorio
        records = self.biometric_repository.get_by_user_id_and_type(db, user_id, data_type)
        if not records:
            return {"status": "No hay datos para analizar"}
        
        # 2. Convertir a un formato que el análisis pueda entender
        values = [rec.value for rec in records]
        dates = [rec.fechaRegistro for rec in records]
        
        # 3. Realizar la lógica de análisis
        # Aquí es donde podrías usar librerías como NumPy o Pandas para un análisis más profundo.
        latest_value = values[-1] if values else None
        initial_value = values[0] if values else None
        
        if initial_value is not None:
            # Calcular el cambio porcentual
            if initial_value != 0:
                change_percentage = ((latest_value - initial_value) / initial_value) * 100
            else:
                change_percentage = 0
        else:
            change_percentage = 0
            
        # 4. Devolver un reporte estructurado
        return {
            "userId": user_id,
            "dataType": data_type,
            "latestValue": latest_value,
            "initialValue": initial_value,
            "changePercentage": round(change_percentage, 2),
            "totalRecords": len(records)
        }