import requests

# Configurações
API_URL = "http://localhost:8000"

def test_listar_funcionarios():
    """Testa a listagem de funcionários na API"""
    
    # Primeiro fazer login para obter o token
    login_data = {
        "username": "admin@exemplo.com",
        "password": "senha123"
    }
    
    login_response = requests.post(f"{API_URL}/auth/login", data=login_data)
    assert login_response.status_code == 200, f"Falha no login: {login_response.text}"
    
    # Extrair o token
    token = login_response.json()["access_token"]
    
    # Configurando o cabeçalho com o token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # Fazendo a requisição para listar funcionários
    response = requests.get(f"{API_URL}/funcionarios/", headers=headers)
    
    # Verificando se a listagem foi bem-sucedida
    assert response.status_code == 200, f"Falha ao listar funcionários: {response.text}"
    
    # Verificando se os dados retornados são uma lista
    funcionarios = response.json()
    assert isinstance(funcionarios, list), "Resposta não é uma lista"
    
    # Imprimindo informações sobre os funcionários encontrados
    print(f"✅ Teste de listagem de funcionários concluído com sucesso")
    print(f"Foram encontrados {len(funcionarios)} funcionários")
    
    # Se houver funcionários, mostrar o primeiro como exemplo
    if funcionarios:
        print("Exemplo do primeiro funcionário:")
        print(f"Código: {funcionarios[0]['codigo']}")
        print(f"Nome: {funcionarios[0]['nome']}")
        print(f"Empresa: {funcionarios[0]['nomeempresa']}")
    
    return funcionarios

if __name__ == "__main__":
    test_listar_funcionarios()