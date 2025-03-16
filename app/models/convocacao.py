from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Convocacao(Base):
    __tablename__ = "convocacoes"
    
    id = Column(Integer, primary_key=True, index=True)
    codigoempresa = Column(Integer, ForeignKey("empresas.codigo"), nullable=False)
    nomeabreviado = Column(String(100))
    unidade = Column(String(150))
    cidade = Column(String(100))
    estado = Column(String(50))
    bairro = Column(String(100))
    endereco = Column(String(200))
    cep = Column(String(20))
    cnpjunidade = Column(String(20))
    setor = Column(String(100))
    cargo = Column(String(100))
    codigofuncionario = Column(Integer, ForeignKey("funcionarios.codigo"), nullable=False)
    cpffuncionario = Column(String(20))
    matricula = Column(String(50))
    dataadmissao = Column(Date)
    nome = Column(String(150))
    emailfuncionario = Column(String(100))
    telefonefuncionario = Column(String(50))
    codigoexame = Column(String(50))
    exame = Column(String(200))
    ultimopedido = Column(Date)
    dataresultado = Column(Date)
    periodicidade = Column(Integer)  # Em meses
    refazer = Column(Integer, default=0)  # 0 = Não, 1 = Sim
    
    # Relacionamentos
    empresa = relationship("Empresa", back_populates="convocacoes")
    funcionario = relationship("Funcionario", back_populates="convocacoes")