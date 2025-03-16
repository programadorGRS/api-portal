from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .database import engine, Base
from .routers import auth, usuarios, empresas, funcionarios, convocacoes, absenteismos

# Criar todas as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# Configurar o limitador de requisições
limiter = Limiter(key_func=get_remote_address)

# Criar a aplicação FastAPI
app = FastAPI(
    title="API Portal GRS",
    description="API para o Portal GRS com FastAPI",
    version="0.1.0"
)

# Adicionar o limitador de requisições como um manipulador de exceção
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restringir para as origens necessárias
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Adicionar os roteadores
app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(empresas.router)
app.include_router(funcionarios.router)
app.include_router(convocacoes.router)
app.include_router(absenteismos.router)

@app.get("/")
@limiter.limit("10/minute")
def root(request: Request):
    return {"message": "Bem-vindo à API do Portal GRS"}