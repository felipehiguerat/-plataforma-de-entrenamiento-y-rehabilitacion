
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.domain.schemas.schemas import BiometricRead,BiometricCreate

from app.domain.models.models import Biometric as BiometricModel


class BiometricRepository:

    def create(self, db: Session, biometric: BiometricCreate) -> BiometricCreate:
        """Crea un nuevo registro biométrico en la base de datos."""
        db_biometric = BiometricModel(**biometric.model_dump())
        db.add(db_biometric)
        db.commit()
        db.refresh(db_biometric)
        return db_biometric

    def get_by_id(self, db: Session, biometric_id: UUID) -> Optional[BiometricRead]:
        """Obtiene un registro biométrico por su ID."""
        return db.query(BiometricModel).filter(BiometricModel.biometricId == biometric_id).first()
    
    def get_by_user_id(self, db: Session, user_id: UUID) -> List[BiometricRead]:
        """Obtiene todos los registros biométricos de un usuario."""
        return db.query(BiometricModel).filter(BiometricModel.userId == user_id).all()

    def get_by_user_id_and_type(self, db: Session, user_id: UUID, data_type: str) -> List[BiometricModel]:
        """Obtiene registros biométricos de un usuario por el tipo de dato (ej. 'peso', 'talla')."""
        return db.query(BiometricModel).filter(
            BiometricModel.userId == user_id,
            BiometricModel.dataType == data_type
        ).all()

    def update(self, db: Session, biometric_id: UUID, biometric_update: BiometricRead) -> Optional[BiometricModel]:
        """Actualiza un registro biométrico existente."""
        db_biometric = self.get_by_id(db, biometric_id)
        if db_biometric:
            for key, value in biometric_update.model_dump(exclude_unset=True).items():
                setattr(db_biometric, key, value)
            db.commit()
            db.refresh(db_biometric)
        return db_biometric

    def delete(self, db: Session, biometric_id: UUID) -> Optional[BiometricModel]:
        """Elimina un registro biométrico por su ID."""
        db_biometric = self.get_by_id(db, biometric_id)
        if db_biometric:
            db.delete(db_biometric)
            db.commit()
        return db_biometric
  
    async def get_by_user_name(self, db: Session, user_name: str) -> List[BiometricRead]:
        """
        Obtiene todos los registros biométricos de un usuario buscando por su nombre.
        Orquesta la comunicación con el microservicio de autenticación.
        """
        # 1. Lógica de negocio: Obtener el UUID del usuario a través del servicio externo.
        user_profile = await self.user_service.get_user_by_name(user_name)
        if not user_profile:
            # Puedes manejar esto con un HTTPException en la ruta
            return None 

        user_id = user_profile.get("id")
        
        # 2. El servicio usa el repositorio para obtener los datos con el ID ya resuelto.
        return self.biometric_repository.get_by_user_id(db, user_id)


