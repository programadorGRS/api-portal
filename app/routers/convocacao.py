from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ..database import get_db
from ..models.usuario import Usuario
from ..models.convocacao import Convocacao
from ..models.funcionario import Funcionario
from ..schemas.convocacao import ConvocacaoCreate, ConvocacaoUpdate, Convocacao as ConvocacaoSchema
from ..core.security import obter_usuario_atual

router = APIRouter(
    prefix="/convocacoes",
    tags=["convocações"],
    dependencies=[Depends(obter_usuario_atual)],
)

@router.get("/", response_model=List[ConvocacaoSchema])
def listar_convocacoes(
    skip: int = 0,
    limit: int = 100,
    empresa_id: Optional[int] = None,
    funcionario_id: Optional[int] = None,
    codigoexame: Optional[str] = None,
    refazer: Optional[int] = None,
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Lista convocações com filtros opcionais.
    Requer permissão de administrador, clienteadm ou convocacao.
    """
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "convocacao"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar convocações"
        )
    
    # Construir a consulta base
    query = db.query(Convocacao)
    
    # Se não for administrador, filtrar por empresas do usuário
    if usuario_atual.tipo != "administrador":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        query = query.filter(Convocacao.codigoempresa.in_(empresas_permitidas))
    
    # Aplicar filtros
    if empresa_id:
        query = query.filter(Convocacao.codigoempresa == empresa_id)
    if funcionario_id:
        query = query.filter(Convocacao.codigofuncionario == funcionario_id)
    if codigoexame:
        query = query.filter(Convocacao.codigoexame == codigoexame)
    if refazer is not None:
        query = query.filter(Convocacao.refazer == refazer)
    if data_inicio:
        query = query.filter(Convocacao.ultimopedido >= data_inicio)
    if data_fim:
        query = query.filter(Convocacao.ultimopedido <= data_fim)
    
    # Retornar resultados paginados
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=ConvocacaoSchema)
def criar_convocacao(
    convocacao: ConvocacaoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Cria uma nova convocação.
    Requer permissão de administrador, clienteadm ou convocacao.
    """
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "convocacao"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para criar convocações"
        )
    
    # Se não for administrador, verificar se a empresa está nas permitidas
    if usuario_atual.tipo != "administrador":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if convocacao.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para criar convocações para esta empresa"
            )
    
    # Verificar se funcionário existe
    funcionario = db.query(Funcionario).filter(Funcionario.codigo == convocacao.codigofuncionario).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    
    # Criar a convocação
    db_convocacao = Convocacao(**convocacao.dict())
    db.add(db_convocacao)
    db.commit()
    db.refresh(db_convocacao)
    
    return db_convocacao

@router.get("/{convocacao_id}", response_model=ConvocacaoSchema)
def ler_convocacao(
    convocacao_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Obtém detalhes de uma convocação específica.
    Requer permissão de administrador, clienteadm ou convocacao.
    """
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "convocacao"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar convocações"
        )
    
    # Buscar a convocação
    convocacao = db.query(Convocacao).filter(Convocacao.id == convocacao_id).first()
    if not convocacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Convocação não encontrada"
        )
    
    # Se não for administrador, verificar se a empresa está nas permitidas
    if usuario_atual.tipo != "administrador":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if convocacao.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para acessar esta convocação"
            )
    
    return convocacao

@router.put("/{convocacao_id}", response_model=ConvocacaoSchema)
def atualizar_convocacao(
    convocacao_id: int,
    convocacao: ConvocacaoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Atualiza uma convocação existente.
    Requer permissão de administrador, clienteadm ou convocacao.
    """
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "convocacao"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para atualizar convocações"
        )
    
    # Buscar a convocação
    db_convocacao = db.query(Convocacao).filter(Convocacao.id == convocacao_id).first()
    if not db_convocacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Convocação não encontrada"
        )
    
    # Se não for administrador, verificar se a empresa está nas permitidas
    if usuario_atual.tipo != "administrador":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if db_convocacao.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para atualizar esta convocação"
            )
    
    # Atualizar dados
    for key, value in convocacao.dict(exclude_unset=True).items():
        setattr(db_convocacao, key, value)
    
    db.commit()
    db.refresh(db_convocacao)
    return db_convocacao

@router.delete("/{convocacao_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_convocacao(
    convocacao_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    """
    Remove uma convocação.
    Requer permissão de administrador ou clienteadm.
    """
    # Verificar permissões (apenas administrador e clienteadm podem deletar)
    if usuario_atual.tipo not in ["administrador", "clienteadm"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar convocações"
        )
    
    # Buscar a convocação
    convocacao = db.query(Convocacao).filter(Convocacao.id == convocacao_id).first()
    if not convocacao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Convocação não encontrada"
        )
    
    # Se for clienteadm, verificar se a empresa está nas permitidas
    if usuario_atual.tipo == "clienteadm":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if convocacao.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para deletar esta convocação"
            )
    
    # Deletar a convocação
    db.delete(convocacao)
    db.commit()
    
    return None