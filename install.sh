#!/bin/bash

echo "======================================"
echo "Script de Instalação - API IPMA"
echo "======================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null
then
    echo "ERRO: Python 3 não encontrado. Por favor, instale o Python 3.8 ou superior."
    exit 1
fi

echo "Python encontrado: $(python3 --version)"
echo ""

# Criar ambiente virtual
echo "1. Criando ambiente virtual..."
python3 -m venv venv

if [ $? -eq 0 ]; then
    echo "   Ambiente virtual criado com sucesso!"
else
    echo "   ERRO ao criar ambiente virtual."
    exit 1
fi

# Ativar ambiente virtual
echo ""
echo "2. Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo ""
echo "3. Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "   Dependências instaladas com sucesso!"
else
    echo "   ERRO ao instalar dependências."
    exit 1
fi

# Copiar ficheiro de ambiente
echo ""
echo "4. Configurando variáveis de ambiente..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "   Ficheiro .env criado!"
else
    echo "   Ficheiro .env já existe."
fi

echo ""
echo "======================================"
echo "Instalação concluída com sucesso!"
echo "======================================"
echo ""
echo "Para executar a aplicação:"
echo "  1. Ative o ambiente virtual: source venv/bin/activate"
echo "  2. Execute: python app.py"
echo ""
"""
Script de teste para verificar os endpoints da API
"""
import requests
import json


BASE_URL = "http://localhost:5000"


def print_response(titulo, response):
    """Imprime a resposta de forma formatada"""
    print(f"\n{'='*60}")
    print(f"{titulo}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Resposta:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


def testar_api():
    """Testa todos os endpoints da API"""

    print("Iniciando testes da API...")

    # Teste 1: Endpoint raiz
    try:
        response = requests.get(f"{BASE_URL}/")
        print_response("Teste 1: Informações da API", response)
    except Exception as e:
        print(f"Erro no teste 1: {e}")

    # Teste 2: Listar distritos
    try:
        response = requests.get(f"{BASE_URL}/distritos")
        print_response("Teste 2: Listar Distritos", response)
    except Exception as e:
        print(f"Erro no teste 2: {e}")

    # Teste 3: Listar todas as localidades
    try:
        response = requests.get(f"{BASE_URL}/localidades")
        print_response("Teste 3: Listar Todas as Localidades", response)
    except Exception as e:
        print(f"Erro no teste 3: {e}")

    # Teste 4: Listar localidades de Lisboa (distrito_id=11)
    try:
        response = requests.get(f"{BASE_URL}/localidades?distrito_id=11")
        print_response("Teste 4: Localidades de Lisboa", response)
    except Exception as e:
        print(f"Erro no teste 4: {e}")

    # Teste 5: Previsão para Lisboa (ID: 1110600)
    try:
        response = requests.get(f"{BASE_URL}/previsao/1110600")
        print_response("Teste 5: Previsão para Lisboa", response)
    except Exception as e:
        print(f"Erro no teste 5: {e}")

    # Teste 6: Previsão com parâmetros de query
    try:
        response = requests.get(f"{BASE_URL}/previsao?localidade_id=1110600&dias=3")
        print_response("Teste 6: Previsão com Query Parameters", response)
    except Exception as e:
        print(f"Erro no teste 6: {e}")

    print(f"\n{'='*60}")
    print("Testes concluídos!")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    print("\nCertifique-se de que a API está a correr em http://localhost:5000\n")
    input("Pressione Enter para continuar com os testes...")
    testar_api()

