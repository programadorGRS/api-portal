from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Absenteismo(Base):
    __tablename__ = "absenteismos"
    
    id = Column(Integer, primary_key=True, index=True)
    unidade = Column(String(130))
    setor = Column(String(130))
    # Usaremos uma coluna separada para matricula e relacionamento
    matricula_func = Column(String(30))
    # Adicionar a chave estrangeira para o ID do funcionário
    funcionario_id = Column(Integer, ForeignKey("funcionarios.codigo"))
    dt_nascimento = Column(Date)
    sexo = Column(Integer)
    tipo_atestado = Column(Integer)
    dt_inicio_atestado = Column(Date)
    dt_fim_atestado = Column(Date)
    hora_inicio_atestado = Column(String(5))
    hora_fim_atestado = Column(String(5))
    dias_afastados = Column(Integer)
    horas_afastado = Column(String(5))
    cid_principal = Column(String(10))
    descricao_cid = Column(String(264))
    grupo_patologico = Column(String(80))
    tipo_licenca = Column(String(100))
    
    # Relacionamentos
    funcionario = relationship("Funcionario", back_populates="absenteismos")