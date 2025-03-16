from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.usuario import Usuario
from ..models.empresa import Empresa
from ..schemas.empresa import EmpresaCreate, EmpresaUpdate, Empresa as EmpresaSchema
from ..core.security import obter_usuario_atual

router = APIRouter(
    prefix="/empresas",
    tags=["empresas"],
    dependencies=[Depends(obter_usuario_atual)],
)

@router.get("/", response_model=List[EmpresaSchema])
def listar_empresas(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Administrador vê todas as empresas
    if usuario_atual.tipo == "administrador":
        return db.query(Empresa).offset(skip).limit(limit).all()
    
    # Outros usuários veem apenas suas empresas
    return usuario_atual.empresas

@router.post("/", response_model=EmpresaSchema)
def criar_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissão (apenas administrador pode criar empresas)
    if usuario_atual.tipo != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem criar empresas"
        )
    
    # Verificar se o CNPJ já existe
    db_empresa = db.query(Empresa).filter(Empresa.cnpj == empresa.cnpj).first()
    if db_empresa:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CNPJ já cadastrado"
        )
    
    # Criar a empresa
    db_empresa = Empresa(**empresa.dict())
    db.add(db_empresa)
    db.commit()
    db.refresh(db_empresa)
    
    return db_empresa

@router.get("/{empresa_id}", response_model=EmpresaSchema)
def ler_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Buscar a empresa
    empresa = db.query(Empresa).filter(Empresa.codigo == empresa_id).first()
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    # Verificar permissão
    if usuario_atual.tipo != "administrador" and empresa not in usuario_atual.empresas:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para acessar esta empresa"
        )
    
    return empresa

@router.put("/{empresa_id}", response_model=EmpresaSchema)
def atualizar_empresa(
    empresa_id: int,
    empresa: EmpresaUpdate,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissão (apenas administrador pode atualizar empresas)
    if usuario_atual.tipo != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem atualizar empresas"
        )
    
    # Buscar a empresa
    db_empresa = db.query(Empresa).filter(Empresa.codigo == empresa_id).first()
    if not db_empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    # Atualizar dados
    for key, value in empresa.dict(exclude_unset=True).items():
        setattr(db_empresa, key, value)
    
    db.commit()
    db.refresh(db_empresa)
    return db_empresa

@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_empresa(
    empresa_id: int,
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissão (apenas administrador pode deletar empresas)
    if usuario_atual.tipo != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem deletar empresas"
        )
    
    # Buscar a empresa
    empresa = db.query(Empresa).filter(Empresa.codigo == empresa_id).first()
    if not empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empresa não encontrada"
        )
    
    # Verificar se há usuários vinculados à empresa
    if empresa.usuarios:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar uma empresa com usuários vinculados"
        )
    
    # Deletar a empresa
    db.delete(empresa)
    db.commit()
    
    return None