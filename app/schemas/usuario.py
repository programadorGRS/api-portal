from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    tipo: str
    empresa_principal_id: Optional[int] = None

    @validator('tipo')
    def validar_tipo(cls, v):
        tipos_validos = ['administrador', 'clienteadm', 'convocacao', 'absenteismo', 'funcionarios']
        if v not in tipos_validos:
            raise ValueError(f'Tipo deve ser um dos seguintes: {", ".join(tipos_validos)}')
        return v

class UsuarioCreate(UsuarioBase):
    senha: str
    empresas_ids: Optional[List[int]] = []

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    tipo: Optional[str] = None
    empresa_principal_id: Optional[int] = None
    empresas_ids: Optional[List[int]] = None
    
    @validator('tipo')
    def validar_tipo(cls, v):
        if v is not None:
            tipos_validos = ['administrador', 'clienteadm', 'convocacao', 'absenteismo', 'funcionarios']
            if v not in tipos_validos:
                raise ValueError(f'Tipo deve ser um dos seguintes: {", ".join(tipos_validos)}')
        return v

class UsuarioInDB(UsuarioBase):
    id: int
    data_criacao: datetime
    ultimo_acesso: Optional[datetime] = None

    class Config:
        from_attributes = True 

class Usuario(UsuarioInDB):
    pass