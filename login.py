import requests

# Configurações
API_URL = "http://localhost:8000"

def test_login():
    """Testa o processo de login na API"""
    
    # Dados de login
    login_data = {
        "username": "programador@grsnucleo.com.br",
        "password": "pokemon230"
    }
    
    # Fazendo a requisição de login
    response = requests.post(f"{API_URL}/auth/login", data=login_data)
    
    # Verificando se o login foi bem-sucedido
    assert response.status_code == 200, f"Falha no login: {response.text}"
    
    # Verificando se o token foi retornado
    data = response.json()
    assert "access_token" in data, "Token não encontrado na resposta"
    assert "token_type" in data, "Tipo de token não encontrado na resposta"
    
    print("✅ Teste de login concluído com sucesso")
    return data["access_token"]

if __name__ == "__main__":
    token = test_login()
    print(f"Token obtido: {token}")