from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from .usuario import usuario_empresa

class Empresa(Base):
    __tablename__ = "empresas"
    
    codigo = Column(Integer, primary_key=True, index=True)
    nomeabreviado = Column(String(60), nullable=False)
    razaosocialinicial = Column(String(200))
    razaosocial = Column(String(200), nullable=False)
    endereco = Column(String(110))
    numeroendereco = Column(String(20))
    complementoendereco = Column(String(300))
    bairro = Column(String(80))
    cidade = Column(String(50))
    cep = Column(String(11))
    uf = Column(String(2))
    cnpj = Column(String(20), unique=True, nullable=False)
    inscricaoestadual = Column(String(20))
    inscricaomunicipal = Column(String(20))
    ativo = Column(Integer, default=1)
    
    # Relacionamentos
    usuarios = relationship("Usuario", secondary=usuario_empresa, back_populates="empresas")
    funcionarios = relationship("Funcionario", back_populates="empresa")
    convocacoes = relationship("Convocacao", back_populates="empresa")