from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime

class EmpresaBase(BaseModel):
    nomeabreviado: str
    razaosocialinicial: Optional[str] = None
    razaosocial: str
    endereco: Optional[str] = None
    numeroendereco: Optional[str] = None
    complementoendereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    uf: Optional[str] = None
    cnpj: str
    inscricaoestadual: Optional[str] = None
    inscricaomunicipal: Optional[str] = None
    ativo: Optional[int] = 1
    
    @validator('ativo')
    def validar_ativo(cls, v):
        if v not in [0, 1]:
            raise ValueError('Ativo deve ser 0 ou 1')
        return v
        
    @validator('uf')
    def validar_uf(cls, v):
        if v is not None and len(v) != 2:
            raise ValueError('UF deve ter 2 caracteres')
        return v
        
class EmpresaCreate(EmpresaBase):
    pass
    
class EmpresaUpdate(BaseModel):
    nomeabreviado: Optional[str] = None
    razaosocialinicial: Optional[str] = None
    razaosocial: Optional[str] = None
    endereco: Optional[str] = None
    numeroendereco: Optional[str] = None
    complementoendereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    cep: Optional[str] = None
    uf: Optional[str] = None
    cnpj: Optional[str] = None
    inscricaoestadual: Optional[str] = None
    inscricaomunicipal: Optional[str] = None
    ativo: Optional[int] = None
    
    @validator('ativo')
    def validar_ativo(cls, v):
        if v is not None and v not in [0, 1]:
            raise ValueError('Ativo deve ser 0 ou 1')
        return v
        
    @validator('uf')
    def validar_uf(cls, v):
        if v is not None and len(v) != 2:
            raise ValueError('UF deve ter 2 caracteres')
        return v

class Empresa(EmpresaBase):
    codigo: int
    
    class Config:
        from_attributes = True 