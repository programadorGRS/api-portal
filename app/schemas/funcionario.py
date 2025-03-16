from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import date, datetime

# Modelos Base
class FuncionarioBase(BaseModel):
    nome: str
    codigoempresa: int
    nomeempresa: Optional[str] = None
    codigounidade: Optional[str] = None
    nomeunidade: Optional[str] = None
    codigosetor: Optional[str] = None
    nomesetor: Optional[str] = None
    codigocargo: Optional[str] = None
    nomecargo: Optional[str] = None
    cbocargo: Optional[str] = None
    ccusto: Optional[str] = None
    nomecentrocusto: Optional[str] = None
    matriculafuncionario: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    ufrg: Optional[str] = None
    orgaoemissorrg: Optional[str] = None
    situacao: Optional[str] = None
    sexo: Optional[int] = None  # 1-Masculino, 2-Feminino
    pis: Optional[str] = None
    ctps: Optional[str] = None
    seriectps: Optional[str] = None
    estadocivil: Optional[int] = None
    tipocontatacao: Optional[int] = None
    data_nascimento: Optional[date] = None
    data_admissao: Optional[date] = None
    data_demissao: Optional[date] = None
    endereco: Optional[str] = None
    numero_endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefoneresidencial: Optional[str] = None
    telefonecelular: Optional[str] = None
    email: Optional[str] = None
    deficiente: Optional[int] = Field(None, ge=0, le=1)
    deficiencia: Optional[str] = None
    nm_mae_funcionario: Optional[str] = None
    dataultalteracao: Optional[date] = None
    matricularh: Optional[str] = None
    cor: Optional[int] = None
    escolaridade: Optional[int] = None
    naturalidade: Optional[str] = None
    ramal: Optional[str] = None
    regimerevezamento: Optional[int] = None
    regimetrabalho: Optional[str] = None
    telcomercial: Optional[str] = None
    turnotrabalho: Optional[int] = None
    rhunidade: Optional[str] = None
    rhsetor: Optional[str] = None
    rhcargo: Optional[str] = None
    rhcentrocustounidade: Optional[str] = None

    @validator('sexo')
    def validar_sexo(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError('Sexo deve ser 1 (Masculino) ou 2 (Feminino)')
        return v

    @validator('estadocivil')
    def validar_estado_civil(cls, v):
        if v is not None and v not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError('Estado civil inválido')
        return v

# Modelo para criação
class FuncionarioCreate(FuncionarioBase):
    pass

# Modelo para atualização
class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    nomeempresa: Optional[str] = None
    codigounidade: Optional[str] = None
    nomeunidade: Optional[str] = None
    codigosetor: Optional[str] = None
    nomesetor: Optional[str] = None
    codigocargo: Optional[str] = None
    nomecargo: Optional[str] = None
    cbocargo: Optional[str] = None
    ccusto: Optional[str] = None
    nomecentrocusto: Optional[str] = None
    matriculafuncionario: Optional[str] = None
    cpf: Optional[str] = None
    rg: Optional[str] = None
    ufrg: Optional[str] = None
    orgaoemissorrg: Optional[str] = None
    situacao: Optional[str] = None
    sexo: Optional[int] = None
    pis: Optional[str] = None
    ctps: Optional[str] = None
    seriectps: Optional[str] = None
    estadocivil: Optional[int] = None
    tipocontatacao: Optional[int] = None
    data_nascimento: Optional[date] = None
    data_admissao: Optional[date] = None
    data_demissao: Optional[date] = None
    endereco: Optional[str] = None
    numero_endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None
    telefoneresidencial: Optional[str] = None
    telefonecelular: Optional[str] = None
    email: Optional[str] = None
    deficiente: Optional[int] = Field(None, ge=0, le=1)
    deficiencia: Optional[str] = None
    nm_mae_funcionario: Optional[str] = None
    dataultalteracao: Optional[date] = None
    matricularh: Optional[str] = None
    cor: Optional[int] = None
    escolaridade: Optional[int] = None
    naturalidade: Optional[str] = None
    ramal: Optional[str] = None
    regimerevezamento: Optional[int] = None
    regimetrabalho: Optional[str] = None
    telcomercial: Optional[str] = None
    turnotrabalho: Optional[int] = None
    rhunidade: Optional[str] = None
    rhsetor: Optional[str] = None
    rhcargo: Optional[str] = None
    rhcentrocustounidade: Optional[str] = None

    @validator('sexo')
    def validar_sexo(cls, v):
        if v is not None and v not in [1, 2]:
            raise ValueError('Sexo deve ser 1 (Masculino) ou 2 (Feminino)')
        return v

    @validator('estadocivil')
    def validar_estado_civil(cls, v):
        if v is not None and v not in [1, 2, 3, 4, 5, 6, 7]:
            raise ValueError('Estado civil inválido')
        return v

# Modelo para resposta
class Funcionario(FuncionarioBase):
    codigo: int
    data_criacao: datetime
    ultima_atualizacao: datetime

    class Config:
        from_attributes = True