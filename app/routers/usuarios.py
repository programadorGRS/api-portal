from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models.usuario import Usuario
from ..models.empresa import Empresa
from ..schemas.usuario import UsuarioCreate, UsuarioUpdate, Usuario as UsuarioSchema
from ..core.security import obter_usuario_atual, verificar_permissao_admin, gerar_hash_senha

router = APIRouter(
    prefix="/usuarios",
    tags=["usuários"],
    dependencies=[Depends(obter_usuario_atual)],
)

@router.get("/", response_model=List[UsuarioSchema])
def listar_usuarios(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Apenas administradores podem ver todos usuários
    if usuario_atual.tipo == "administrador":
        return db.query(Usuario).offset(skip).limit(limit).all()
    
    # ClienteAdm vê apenas usuários de suas empresas
    if usuario_atual.tipo == "clienteadm":
        empresas_ids = [empresa.codigo for empresa in usuario_atual.empresas]
        return db.query(Usuario).filter(Usuario.empresa_principal_id.in_(empresas_ids)).offset(skip).limit(limit).all()
    
    # Outros usuários veem apenas a si mesmos
    return [usuario_atual]

@router.post("/", response_model=UsuarioSchema)
def criar_usuario(
    usuario: UsuarioCreate, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissão de administrador ou clienteadm
    if usuario_atual.tipo not in ["administrador", "clienteadm"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sem permissão para criar usuários"
        )
    
    # Verificar se email já existe
    db_usuario = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if db_usuario:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    # Verificar se empresas existem
    if usuario.empresas_ids:
        empresas = db.query(Empresa).filter(Empresa.codigo.in_(usuario.empresas_ids)).all()
        if len(empresas) != len(usuario.empresas_ids):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uma ou mais empresas não existem"
            )
    
    # Criar o usuário
    senha_hash = gerar_hash_senha(usuario.senha)
    db_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha_hash=senha_hash,
        tipo=usuario.tipo,
        empresa_principal_id=usuario.empresa_principal_id
    )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    # Adicionar empresas ao usuário
    if usuario.empresas_ids:
        for empresa in empresas:
            db_usuario.empresas.append(empresa)
        db.commit()
        db.refresh(db_usuario)
    
    return db_usuario

@router.get("/{usuario_id}", response_model=UsuarioSchema)
def ler_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões
    if usuario_atual.tipo != "administrador" and usuario_atual.id != usuario_id:
        if usuario_atual.tipo == "clienteadm":
            # ClienteAdm pode ver usuários de suas empresas
            usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario or usuario.empresa_principal_id not in [e.codigo for e in usuario_atual.empresas]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sem permissão para acessar este usuário"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para acessar este usuário"
            )
    
    # Buscar o usuário
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioSchema)
def atualizar_usuario(
    usuario_id: int, 
    usuario: UsuarioUpdate, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Verificar permissões
    if usuario_atual.tipo != "administrador" and usuario_atual.id != usuario_id:
        if usuario_atual.tipo == "clienteadm":
            # ClienteAdm pode atualizar usuários de suas empresas
            db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not db_usuario or db_usuario.empresa_principal_id not in [e.codigo for e in usuario_atual.empresas]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sem permissão para atualizar este usuário"
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Sem permissão para atualizar este usuário"
            )
    
    # Buscar o usuário
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not db_usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Atualizar dados
    for key, value in usuario.dict(exclude_unset=True).items():
        if key == "empresas_ids" and value is not None:
            # Atualizar empresas
            empresas = db.query(Empresa).filter(Empresa.codigo.in_(value)).all()
            if len(empresas) != len(value):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Uma ou mais empresas não existem"
                )
            
            db_usuario.empresas = empresas
        elif key != "empresas_ids":
            setattr(db_usuario, key, value)
    
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_usuario(
    usuario_id: int, 
    db: Session = Depends(get_db),
    usuario_atual: Usuario = Depends(obter_usuario_atual)
):
    # Apenas administrador pode deletar usuários
    if usuario_atual.tipo != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas administradores podem deletar usuários"
        )
    
    # Buscar o usuário
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    # Não permitir deletar a si mesmo
    if usuario.id == usuario_atual.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível deletar o próprio usuário"
        )
    
    # Deletar o usuário
    db.delete(usuario)
    db.commit()
    
    return None