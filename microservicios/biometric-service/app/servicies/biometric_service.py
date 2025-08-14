# app/services/biometric_service.py
from _pytest.logging import logging
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List, Dict, Any
from datetime import datetime, timedelta
from app.domain.schemas.schemas import BiometricRead,BiometricBase,BiometricCreateData, BiometricUpdate,BiometricCreateRequest
from app.repository.bometric_repo import BiometricRepository
from app.servicies.user_service import get_user_by_username

logger = logging.getLogger(__name__)

class BiometricService:
    def __init__(self, biometric_repository: BiometricRepository):
        self.biometric_repository = biometric_repository

    async def create_new_record(self, db: Session, data: BiometricCreateRequest) -> BiometricRead:
      
        user = await get_user_by_username(data.username)
        if not user:
            raise ValueError(f"User with username '{data.username}' not found.")
        
        biometric_data = BiometricCreateData(
            userId=user['id'],
            username=data.username,
            peso=data.peso,
            talla=data.talla,
            edad=data.edad,
            genero=data.genero,
            imc=None # Se calculará a continuación
        )

        # 3. Lógica de negocio para calcular el IMC
        if biometric_data.talla and biometric_data.peso:
            biometric_data.imc = biometric_data.peso / (biometric_data.talla ** 2)

        logger.info(f"Procesando nuevo registro biométrico para el usuario: {data.username} (ID: {biometric_data.userId})")
        db_biometric = self.biometric_repository.create(db, biometric_data)
        
        return BiometricRead.model_validate(db_biometric)
        
       

    def get_biometric_data_by_user(self, db: Session, user_id: UUID) -> List[BiometricRead]:
        return self.biometric_repository.get_by_user_id(db, user_id)

    async def get_by_user_name(self, db: Session, user_name: str) -> List[BiometricRead]:
        """
        Obtiene los registros biométricos de un usuario buscando por su nombre,
        usando la función importada.
        """
        user_profile = await get_user_by_username(user_name)
        if not user_profile:
            return None 

        user_id = user_profile.get("id")
        return self.biometric_repository.get_by_user_id(db, user_id)
    
    def analyze_progress(self, db: Session, user_id: UUID, data_type: str) -> Dict[str, Any]:
        # ... (la lógica de análisis sigue igual)
        pass # Reemplaza con tu código de análisis

    
    def update_record(self, db: Session, biometric_id: UUID, update_data: BiometricUpdate) ->BiometricRead:
        """
        Busca un registro biométrico por su ID, actualiza sus campos y lo guarda.
        """
        db_biometric = self.biometric_repository.get_by_id(db, biometric_id)
        if not db_biometric:
            return None

        # Actualiza el objeto SQLAlchemy con los datos del Pydantic schema
        # `model_dump` convierte el Pydantic schema en un diccionario
        update_data_dict = update_data.model_dump(exclude_unset=True)
        for key, value in update_data_dict.items():
            setattr(db_biometric, key, value)

        db.commit()
        db.refresh(db_biometric)
        return BiometricRead.model_validate(db_biometric)


    def delete_record(self, db: Session, biometric_id: UUID) -> bool:
        # ... (código para eliminar un registro)
        db_biometric = self.biometric_repository.get_by_id(db, biometric_id)
        if not db_biometric:
            return False

        db.delete(db_biometric)
        db.commit()
        return True