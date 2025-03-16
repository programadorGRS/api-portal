from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

# Tabela de associação entre usuários e empresas
usuario_empresa = Table(
    'usuario_empresa',
    Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuarios.id')),
    Column('empresa_id', Integer, ForeignKey('empresas.codigo'))
)

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    senha_hash = Column(String(255), nullable=False)
    tipo = Column(String(20), nullable=False)  # administrador, clienteadm, convocacao, absenteismo, funcionarios
    empresa_principal_id = Column(Integer, ForeignKey("empresas.codigo"), nullable=True)
    data_criacao = Column(DateTime, default=func.now())
    ultimo_acesso = Column(DateTime, nullable=True)
    
    # Relacionamentos
    empresa_principal = relationship("Empresa", foreign_keys=[empresa_principal_id])
    empresas = relationship("Empresa", secondary=usuario_empresa, back_populates="usuarios")