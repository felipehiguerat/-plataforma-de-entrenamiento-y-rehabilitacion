from pydantic import BaseModel, ConfigDict, Field, field_validator
from typing import Optional
from uuid import UUID
from datetime import datetime


class BiometricBase(BaseModel):
    pass
class BiometricCreateData(BiometricBase):
    userId: Optional[UUID] = None
    username: str
    edad: int
    genero: str
    talla: float = Field(..., gt=0, description="Talla en metros")
    peso: float = Field(..., gt=0, description="Peso en kilogramos")
    imc: Optional[float] = None
    grasaCorporal: Optional[float] = None
    masaMuscular: Optional[float] = None
    # CORRECCIÓN: Los campos ahora coinciden con el modelo
    presionSistolica: Optional[int] = None
    presionDiastolica: Optional[int] = None
    frecuenciaCardiaca: Optional[int] = None

    @field_validator('imc', mode='before')
    def _calculate_imc(cls, v, info):
        if info.data.get('talla') and info.data.get('peso'):
            talla_metros = info.data['talla']
            peso_kg = info.data['peso']
            if talla_metros > 0:
                return peso_kg / (talla_metros ** 2)
        return v

    model_config = ConfigDict(from_attributes=True)




class BiometricCreateRequest(BaseModel):
    username: str
    peso: float
    talla: float
    edad: int
    genero: str
    imc: Optional[float] = None
    grasaCorporal: Optional[float] = None
    masaMuscular: Optional[float] = None
    presionSistolica: Optional[int] = None
    presionDiastolica: Optional[int] = None
    frecuenciaCardiaca: Optional[int] = None

    
    
    imc: Optional[float] = None

class BiometricRead(BiometricBase):
    userId: Optional[UUID] = None
    biometricId: UUID
    username: str
    talla: float = Field(..., gt=0, description="Talla en metros")
    peso: float = Field(..., gt=0, description="Peso en kilogramos")
    edad: int
    genero: str
    imc: Optional[float] = None
    grasaCorporal: Optional[float] = None
    masaMuscular: Optional[float] = None
    presionSistolica: Optional[int] = None
    presionDiastolica: Optional[int] = None
    frecuenciaCardiaca: Optional[int] = None

class BiometricUpdate(BaseModel):
    username: str
    talla: Optional[float] = Field(None, gt=0, description="Talla en metros")
    peso: Optional[float] = Field(None, gt=0, description="Peso en kilogramos")
    edad: Optional[int] = None
    genero: Optional[str] = None
    imc: Optional[float] = None
    grasaCorporal: Optional[float] = None
    masaMuscular: Optional[float] = None
    presionSistolica: Optional[int] = None
    presionDiastolica: Optional[int] = None
    frecuenciaCardiaca: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('imc', mode='before')
    def _calculate_imc(cls, v, info):
        # Validador para calcular el IMC si se actualiza la talla o el peso
        if info.data.get('talla') or info.data.get('peso'):
            talla_metros = info.data.get('talla')
            peso_kg = info.data.get('peso')

            # Si se actualizan ambos, se usa la fórmula
            if talla_metros and peso_kg and talla_metros > 0:
                return peso_kg / (talla_metros ** 2)

        return v
    
class BiometricDelete(BaseModel):
   username: str


model_config = ConfigDict(from_attributes=True)