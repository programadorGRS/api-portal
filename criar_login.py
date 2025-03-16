from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models.usuario import Usuario
from app.core.security import gerar_hash_senha
import sys

def criar_admin(email, senha, nome):
    """Cria um usuário administrador diretamente no banco de dados"""
    db = SessionLocal()
    try:
        usuario_existente = db.query(Usuario).filter(Usuario.email == email).first()
        if usuario_existente:
            print(f"Usuário com email {email} já existe!")
            return False
        
        senha_hash = gerar_hash_senha(senha)

        admin = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            tipo="administrador"
        )
        
        db.add(admin)
        db.commit()
        print(f"Usuário administrador criado com sucesso: {email}")
        return True
    except Exception as e:
        print(f"Erro ao criar usuário: {e}")
        return False
    finally:
        db.close()

if __name__ == "__main__":

    
    email = 'programador@grsnucleo.com.br'
    senha = 'pokemon230'
    nome = 'Henrique Siqueira'
    
    criar_admin(email, senha, nome)