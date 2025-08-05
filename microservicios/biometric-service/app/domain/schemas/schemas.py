from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime

# Esquema base con los campos comunes
class BiometricBase(BaseModel):
    userId: UUID
    talla: float = Field(..., gt=0, description="Talla en metros")
    peso: float = Field(..., gt=0, description="Peso en kilogramos")
    imc: Optional[float] = None
    grasaCorporal: Optional[float] = None
    masaMuscular: Optional[float] = None
    presionArterial: Optional[str] = None
    frecuenciaCardiaca: Optional[int] = None


    @field_validator('imc', mode='before')
    def _calculate_imc(cls, v, info):
        # El validador calcula el IMC si se le pasa talla y peso.
        if info.data.get('talla') and info.data.get('peso'):
            talla_metros = info.data['talla']
            peso_kg = info.data['peso']
            if talla_metros > 0:
                # La fórmula del IMC es peso / (talla * talla)
                return peso_kg / (talla_metros ** 2)
        return v


class BiometricCreate(BiometricBase):
    pass

class BiometricRead(BiometricBase):
    biometricId: UUID
    fechaRegistro: datetime

model_config = ConfigDict(from_attributes=True)