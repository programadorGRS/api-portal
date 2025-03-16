from app.database import Base, engine
from app.models.usuario import Usuario
from app.models.empresa import Empresa
from app.models.funcionario import Funcionario
from app.models.convocacao import Convocacao

def criar_tabelas():
    """Cria todas as tabelas no banco de dados"""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()