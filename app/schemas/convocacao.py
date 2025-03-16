from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class ConvocacaoBase(BaseModel):
    codigoempresa: int
    codigofuncionario: int
    nomeabreviado: Optional[str] = None
    unidade: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    bairro: Optional[str] = None
    endereco: Optional[str] = None
    cep: Optional[str] = None
    cnpjunidade: Optional[str] = None
    setor: Optional[str] = None
    cargo: Optional[str] = None
    cpffuncionario: Optional[str] = None
    matricula: Optional[str] = None
    dataadmissao: Optional[date] = None
    nome: Optional[str] = None
    emailfuncionario: Optional[str] = None
    telefonefuncionario: Optional[str] = None
    codigoexame: Optional[str] = None
    exame: Optional[str] = None
    ultimopedido: Optional[date] = None
    dataresultado: Optional[date] = None
    periodicidade: Optional[int] = None
    refazer: Optional[int] = 0

    @validator('refazer')
    def validar_refazer(cls, v):
        if v is not None and v not in [0, 1]:
            raise ValueError('Refazer deve ser 0 (Não) ou 1 (Sim)')
        return v

class ConvocacaoCreate(ConvocacaoBase):
    pass

class ConvocacaoUpdate(BaseModel):
    nomeabreviado: Optional[str] = None
    unidade: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    bairro: Optional[str] = None
    endereco: Optional[str] = None
    cep: Optional[str] = None
    cnpjunidade: Optional[str] = None
    setor: Optional[str] = None
    cargo: Optional[str] = None
    cpffuncionario: Optional[str] = None
    matricula: Optional[str] = None
    dataadmissao: Optional[date] = None
    nome: Optional[str] = None
    emailfuncionario: Optional[str] = None
    telefonefuncionario: Optional[str] = None
    codigoexame: Optional[str] = None
    exame: Optional[str] = None
    ultimopedido: Optional[date] = None
    dataresultado: Optional[date] = None
    periodicidade: Optional[int] = None
    refazer: Optional[int] = None

    @validator('refazer')
    def validar_refazer(cls, v):
        if v is not None and v not in [0, 1]:
            raise ValueError('Refazer deve ser 0 (Não) ou 1 (Sim)')
        return v

class Convocacao(ConvocacaoBase):
    id: int

    class Config:
        from_attributes = True