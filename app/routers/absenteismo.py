from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from ..database import get_db
from ..models.usuario import Usuario
from ..models.absenteismo import Absenteismo
from ..models.funcionario import Funcionario
from ..schemas.absenteismo import AbsenteismoCreate, AbsenteismoUpdate, Absenteismo as AbsenteismoSchema
from ..core.security import obter_usuario_atual

router = APIRouter(
    prefix="/absenteismos",
    tags=["absenteísmo"],
    dependencies=[Depends(obter_usuario_atual)],
)

@router.get("/", response_model=List[AbsenteismoSchema])
def listar_absenteismos(
    skip: int = 0,
    limit: int = 100,
    matricula: Optional[str] = None,
    dt_inicio: Optional[date] = None,
    dt_fim: Optional[date] = None,
    tipo_atestado: Optional[int] = None,
    cid: Optional[str] = None,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "absenteismo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar absenteísmo"
        )
    
    # Consulta base
    query = db.query(Absenteismo)
    
    # Aplicar filtros
    if matricula:
        query = query.filter(Absenteismo.matricula_func == matricula)
    if dt_inicio:
        query = query.filter(Absenteismo.dt_inicio_atestado >= dt_inicio)
    if dt_fim:
        query = query.filter(Absenteismo.dt_fim_atestado <= dt_fim)
    if tipo_atestado:
        query = query.filter(Absenteismo.tipo_atestado == tipo_atestado)
    if cid:
        query = query.filter(Absenteismo.cid_principal.like(f"%{cid}%"))
    
    # Se não for administrador, filtrar apenas funcionários das empresas permitidas
    if usuario_atual.tipo != "administrador":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        query = query.join(Funcionario).filter(Funcionario.codigoempresa.in_(empresas_permitidas))
    
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=AbsenteismoSchema)
def criar_absenteismo(
    absenteismo: AbsenteismoCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "absenteismo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para criar registros de absenteísmo"
        )
    
    # Verificar se funcionário existe
    funcionario = db.query(Funcionario).filter(Funcionario.matriculafuncionario == absenteismo.matricula_func).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    
    # Se não for administrador, verificar se tem permissão para a empresa do funcionário
    if usuario_atual.tipo != "administrador":
        empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
        if funcionario.codigoempresa not in empresas_permitidas:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para registrar absenteísmo para este funcionário"
            )
    
    # Criar o registro
    db_absenteismo = Absenteismo(**absenteismo.dict())
    db.add(db_absenteismo)
    db.commit()
    db.refresh(db_absenteismo)
    
    return db_absenteismo

@router.get("/{absenteismo_id}", response_model=AbsenteismoSchema)
def ler_absenteismo(
    absenteismo_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "absenteismo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar absenteísmo"
        )
    
    # Buscar o registro
    absenteismo = db.query(Absenteismo).filter(Absenteismo.id == absenteismo_id).first()
    if not absenteismo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de absenteísmo não encontrado"
        )
    
    # Se não for administrador, verificar permissão
    if usuario_atual.tipo != "administrador":
        funcionario = db.query(Funcionario).filter(Funcionario.matriculafuncionario == absenteismo.matricula_func).first()
        if funcionario:
            empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
            if funcionario.codigoempresa not in empresas_permitidas:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sem permissão para acessar este registro"
                )
    
    return absenteismo

@router.put("/{absenteismo_id}", response_model=AbsenteismoSchema)
def atualizar_absenteismo(
    absenteismo_id: int,
    absenteismo: AbsenteismoUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões
    if usuario_atual.tipo not in ["administrador", "clienteadm", "absenteismo"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para atualizar absenteísmo"
        )
    
    # Buscar o registro
    db_absenteismo = db.query(Absenteismo).filter(Absenteismo.id == absenteismo_id).first()
    if not db_absenteismo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de absenteísmo não encontrado"
        )
    
    # Se não for administrador, verificar permissão
    if usuario_atual.tipo != "administrador":
        funcionario = db.query(Funcionario).filter(Funcionario.matriculafuncionario == db_absenteismo.matricula_func).first()
        if funcionario:
            empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
            if funcionario.codigoempresa not in empresas_permitidas:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sem permissão para atualizar este registro"
                )
    
    # Atualizar dados
    for key, value in absenteismo.dict(exclude_unset=True).items():
        setattr(db_absenteismo, key, value)
    
    db.commit()
    db.refresh(db_absenteismo)
    return db_absenteismo

@router.delete("/{absenteismo_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_absenteismo(
    absenteismo_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões (apenas administrador e clienteadm podem deletar)
    if usuario_atual.tipo not in ["administrador", "clienteadm"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para deletar registros de absenteísmo"
        )
    
    # Buscar o registro
    absenteismo = db.query(Absenteismo).filter(Absenteismo.id == absenteismo_id).first()
    if not absenteismo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro de absenteísmo não encontrado"
        )
    
    # Se for clienteadm, verificar permissão
    if usuario_atual.tipo == "clienteadm":
        funcionario = db.query(Funcionario).filter(Funcionario.matriculafuncionario == absenteismo.matricula_func).first()
        if funcionario:
            empresas_permitidas = [empresa.codigo for empresa in usuario_atual.empresas]
            if funcionario.codigoempresa not in empresas_permitidas:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sem permissão para deletar este registro"
                )
    
    # Deletar o registro
    db.delete(absenteismo)
    db.commit()
    
    return None