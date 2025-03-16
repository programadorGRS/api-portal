from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import timedelta

from ..core.security import verificar_senha, criar_token_acesso, ACCESS_TOKEN_EXPIRE_MINUTES
from ..database import get_db
from ..models.usuario import Usuario
from ..schemas.auth import Token

router = APIRouter(
    prefix="/auth",
    tags=["autenticação"],
    responses={401: {"description": "Não autorizado"}},
)

@router.post("/login", response_model=Token)
async def login_para_token_acesso(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    # Buscar usuário pelo email
    usuario = db.query(Usuario).filter(Usuario.email == form_data.username).first()
    
    # Verificar se o usuário existe e se a senha está correta
    if not usuario or not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Atualizar último acesso
    usuario.ultimo_acesso = func.now()
    db.commit()
    
    # Criar token de acesso
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = criar_token_acesso(
        subject=usuario.id, expires_delta=access_token_expires
    )
    
    return {"access_token": token, "token_type": "bearer"}