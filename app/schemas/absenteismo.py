from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class AbsenteismoBase(BaseModel):
    unidade: Optional[str] = None
    setor: Optional[str] = None
    matricula_func: str
    dt_nascimento: Optional[date] = None
    sexo: Optional[int] = None
    tipo_atestado: Optional[int] = None
    dt_inicio_atestado: Optional[date] = None
    dt_fim_atestado: Optional[date] = None
    hora_inicio_atestado: Optional[str] = None
    hora_fim_atestado: Optional[str] = None
    dias_afastados: Optional[int] = None
    horas_afastado: Optional[str] = None
    cid_principal: Optional[str] = None
    descricao_cid: Optional[str] = None
    grupo_patologico: Optional[str] = None
    tipo_licenca: Optional[str] = None

    @validator('sexo')
    def validar_sexo(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError('Sexo deve ser 1 (Masculino) ou 2 (Feminino)')
        return v

class AbsenteismoCreate(AbsenteismoBase):
    pass

class AbsenteismoUpdate(BaseModel):
    unidade: Optional[str] = None
    setor: Optional[str] = None
    dt_nascimento: Optional[date] = None
    sexo: Optional[int] = None
    tipo_atestado: Optional[int] = None
    dt_inicio_atestado: Optional[date] = None
    dt_fim_atestado: Optional[date] = None
    hora_inicio_atestado: Optional[str] = None
    hora_fim_atestado: Optional[str] = None
    dias_afastados: Optional[int] = None
    horas_afastado: Optional[str] = None
    cid_principal: Optional[str] = None
    descricao_cid: Optional[str] = None
    grupo_patologico: Optional[str] = None
    tipo_licenca: Optional[str] = None

    @validator('sexo')
    def validar_sexo(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError('Sexo deve ser 1 (Masculino) ou 2 (Feminino)')
        return v

class Absenteismo(AbsenteismoBase):
    id: int

    class Config:
        from_attributes = True