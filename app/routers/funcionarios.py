from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.usuario import Usuario
from ..models.empresa import Empresa
from ..models.funcionario import Funcionario
from ..schemas.funcionario import FuncionarioCreate, FuncionarioUpdate, Funcionario as FuncionarioSchema
from ..core.security import obter_usuario_atual

router = APIRouter(
    prefix="/funcionarios",
    tags=["funcionários"],
    dependencies=[Depends(obter_usuario_atual)],
)

@router.get("/", response_model=List[FuncionarioSchema])
def listar_funcionarios(
    skip: int = 0,
    limit: int = 100,
    empresa_id: int = None,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões
    if usuario_atual.tipo == "administrador":
        # Administrador pode ver todos os funcionários (com filtro opcional por empresa)
        query = db.query(Funcionario)
        if empresa_id:
            query = query.filter(Funcionario.codigoempresa == empresa_id)
        return query.offset(skip).limit(limit).all()
    
    # Outros usuários só podem ver funcionários das empresas permitidas
    empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
    
    # Se tipo for "funcionarios", só pode acessar essa funcionalidade
    if usuario_atual.tipo not in ["clienteadm", "funcionarios"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para ver funcionários"
        )
    
    # Se filtro por empresa, verificar se empresa está nas permitidas
    if empresa_id and empresa_id not in empresas_permitidas:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para ver funcionários desta empresa"
        )
    
    # Aplicar filtro de empresas permitidas
    query = db.query(Funcionario).filter(Funcionario.codigoempresa.in_(empresas_permitidas))
    if empresa_id:
        query = query.filter(Funcionario.codigoempresa == empresa_id)
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=FuncionarioSchema)
def criar_funcionario(
    funcionario: FuncionarioCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões (administrador ou clienteadm)
    if usuario_atual.tipo not in ["administrador", "clienteadm"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para criar funcionários"
        )
    
    # Se for clienteadm, verificar se a empresa está nas permitidas
    if usuario_atual.tipo == "clienteadm":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if funcionario.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para criar funcionários nesta empresa"
            )
    
    # Verificar se a empresa existe
    empresa = db.query(Empresa).filter(Empresa.codigo == funcionario.codigoempresa).first()
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    # Criar o funcionário
    db_funcionario = Funcionario(**funcionario.dict())
    db.add(db_funcionario)
    db.commit()
    db.refresh(db_funcionario)
    
    return db_funcionario

@router.get("/{funcionario_id}", response_model=FuncionarioSchema)
def ler_funcionario(
    funcionario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Buscar o funcionário
    funcionario = db.query(Funcionario).filter(Funcionario.codigo == funcionario_id).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    
    # Verificar permissões
    if usuario_atual.tipo == "administrador":
        return funcionario
    
    # Para outros usuários, verificar se a empresa do funcionário está nas permitidas
    empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
    if funcionario.codigoempresa not in empresas_permitidas:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar este funcionário"
        )
    
    # Se tipo for "funcionarios", só pode acessar essa funcionalidade
    if usuario_atual.tipo not in ["clienteadm", "funcionarios"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para ver funcionários"
        )
    
    return funcionario

@router.put("/{funcionario_id}", response_model=FuncionarioSchema)
def atualizar_funcionario(
    funcionario_id: int,
    funcionario: FuncionarioUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões (administrador ou clienteadm)
    if usuario_atual.tipo not in ["administrador", "clienteadm"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para atualizar funcionários"
        )
    
    # Buscar o funcionário
    db_funcionario = db.query(Funcionario).filter(Funcionario.codigo == funcionario_id).first()
    if not db_funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    
    # Se for clienteadm, verificar se a empresa do funcionário está nas permitidas
    if usuario_atual.tipo == "clienteadm":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if db_funcionario.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para atualizar este funcionário"
            )
    
    # Atualizar dados
    for key, value in funcionario.dict(exclude_unset=True).items():
        setattr(db_funcionario, key, value)
    
    db.commit()
    db.refresh(db_funcionario)
    return db_funcionario

@router.delete("/{funcionario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_funcionario(
    funcionario_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões (administrador ou clienteadm)
    if usuario_atual.tipo not in ["administrador", "clienteadm"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar funcionários"
        )
    
    # Buscar o funcionário
    funcionario = db.query(Funcionario).filter(Funcionario.codigo == funcionario_id).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    
    # Se for clienteadm, verificar se a empresa do funcionário está nas permitidas
    if usuario_atual.tipo == "clienteadm":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if funcionario.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para deletar este funcionário"
            )
    
    # Deletar o funcionário
    db.delete(funcionario)
    db.commit()
    
    return None