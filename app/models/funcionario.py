from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Funcionario(Base):
    __tablename__ = "funcionarios"
    
    codigo = Column(Integer, primary_key=True, index=True)
    codigoempresa = Column(Integer, ForeignKey("empresas.codigo"), nullable=False)
    nomeempresa = Column(String(200))
    nome = Column(String(120), nullable=False)
    codigounidade = Column(String(20))
    nomeunidade = Column(String(130))
    codigosetor = Column(String(12))
    nomesetor = Column(String(130))
    codigocargo = Column(String(10))
    nomecargo = Column(String(130))
    cbocargo = Column(String(10))
    ccusto = Column(String(50))
    nomecentrocusto = Column(String(130))
    matriculafuncionario = Column(String(30), unique=True)
    cpf = Column(String(19))
    rg = Column(String(19))
    ufrg = Column(String(10))
    orgaoemissorrg = Column(String(20))
    situacao = Column(String(12))
    sexo = Column(Integer)  # 1-Masculino, 2-Feminino
    pis = Column(String(20))
    ctps = Column(String(30))
    seriectps = Column(String(25))
    estadocivil = Column(Integer)  # 1-Solteiro, 2-Casado, etc.
    tipocontatacao = Column(Integer)
    data_nascimento = Column(Date)
    data_admissao = Column(Date)
    data_demissao = Column(Date)
    endereco = Column(String(110))
    numero_endereco = Column(String(20))
    bairro = Column(String(80))
    cidade = Column(String(50))
    uf = Column(String(20))
    cep = Column(String(10))
    telefoneresidencial = Column(String(20))
    telefonecelular = Column(String(20))
    email = Column(String(400))
    deficiente = Column(Integer)
    deficiencia = Column(String(861))
    nm_mae_funcionario = Column(String(120))
    dataultalteracao = Column(Date)
    matricularh = Column(String(30))
    cor = Column(Integer)
    escolaridade = Column(Integer)
    naturalidade = Column(String(50))
    ramal = Column(String(10))
    regimerevezamento = Column(Integer)
    regimetrabalho = Column(String(500))
    telcomercial = Column(String(20))
    turnotrabalho = Column(Integer)
    rhunidade = Column(String(80))
    rhsetor = Column(String(80))
    rhcargo = Column(String(80))
    rhcentrocustounidade = Column(String(80))
    
    # Metadados
    data_criacao = Column(DateTime, default=func.now())
    ultima_atualizacao = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="funcionarios")
    convocacoes = relationship("Convocacao", back_populates="funcionario")
    absenteismos = relationship("Absenteismo", back_populates="funcionario")