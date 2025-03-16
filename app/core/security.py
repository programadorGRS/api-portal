from datetime import datetime, timedelta
from typing import Any, Union, Optional
from passlib.context import CryptContext
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.usuario import Usuario

# Configurações de segurança
SECRET_KEY = "CHAVE_SUPER_SECRETA_MUDE_ISTO_EM_PRODUCAO"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Bearer token para autenticação OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Funções para senha e token
def verificar_senha(senha_simples: str, senha_hash: str) -> bool:
    return pwd_context.verify(senha_simples, senha_hash)

def gerar_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)

def criar_token_acesso(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependência para obter o usuário atual
async def obter_usuario_atual(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id: str = payload.get("sub")
        if usuario_id is None:
            raise credentials_exception
    except (jwt.JWTError, ValidationError):
        raise credentials_exception
    
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise credentials_exception
    
    return usuario

# Verificar permissões por tipo de usuário
def verificar_permissao_admin(usuario: Usuario):
    if usuario.tipo != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores"
        )