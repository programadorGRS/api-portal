import requests
import json
from datetime import date

# Configurações
API_URL = "http://localhost:8000"

def test_criar_funcionario():
    """Testa a criação de um funcionário na API"""
    
    # Primeiro fazer login para obter o token
    login_data = {
        "username": "admin@exemplo.com",
        "password": "senha123"
    }
    
    login_response = requests.post(f"{API_URL}/auth/login", data=login_data)
    assert login_response.status_code == 200, f"Falha no login: {login_response.text}"
    
    # Extrair o token
    token = login_response.json()["access_token"]
    
    # Dados do funcionário
    funcionario_data = {
        "nome": "José da Silva",
        "codigoempresa": 1,
        "nomeempresa": "Empresa Teste",
        "codigounidade": "UN001",
        "nomeunidade": "Unidade Principal",
        "codigosetor": "SET123",
        "nomesetor": "Setor de Testes",
        "codigocargo": "CG001",
        "nomecargo": "Analista de Testes",
        "cbocargo": "1234-56",
        "cpf": "123.456.789-00",
        "matriculafuncionario": "F12345",
        "sexo": 1,
        "data_admissao": str(date.today()),
        "email": "jose.silva@teste.com"
    }
    
    # Configuração do cabeçalho com o token
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Fazendo a requisição para criar o funcionário
    response = requests.post(
        f"{API_URL}/funcionarios/", 
        headers=headers,
        data=json.dumps(funcionario_data)
    )
    
    # Verificando se a criação foi bem-sucedida
    assert response.status_code in [200, 201], f"Falha ao criar funcionário: {response.text}"
    
    # Verificando se os dados retornados correspondem aos enviados
    created_data = response.json()
    assert created_data["nome"] == funcionario_data["nome"], "Nome do funcionário não corresponde"
    assert created_data["cpf"] == funcionario_data["cpf"], "CPF do funcionário não corresponde"
    
    print("✅ Teste de criação de funcionário concluído com sucesso")
    print(f"Funcionário criado com código: {created_data['codigo']}")
    return created_data["codigo"]

if __name__ == "__main__":
    funcionario_id = test_criar_funcionario()