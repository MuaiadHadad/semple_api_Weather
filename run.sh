#!/bin/bash

# Script de execução da aplicação
# Facilita o início da aplicação

echo "=========================================="
echo "  API de Previsão Meteorológica - IPMA"
echo "=========================================="
echo ""

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo "ERRO: Ambiente virtual não encontrado!"
    echo "Por favor, execute primeiro: ./install.sh"
    exit 1
fi

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se as dependências estão instaladas
if ! python -c "import flask" 2>/dev/null; then
    echo "ERRO: Dependências não instaladas!"
    echo "Por favor, execute: pip install -r requirements.txt"
    exit 1
fi

# Verificar se o ficheiro .env existe
if [ ! -f ".env" ]; then
    echo "Ficheiro .env não encontrado. Criando a partir do exemplo..."
    cp .env.example .env
fi

echo ""
echo "Iniciando aplicação..."
echo "API disponível em: http://localhost:5000"
echo ""
echo "Pressione Ctrl+C para parar a aplicação"
echo "=========================================="
echo ""

# Executar aplicação
python app.py
# Exemplos de Utilização da API

Este documento contém exemplos práticos de como utilizar a API de Previsão Meteorológica do IPMA.

## IDs de Localidades Mais Comuns

Para facilitar os testes, aqui estão os IDs de algumas cidades principais:

- Lisboa: 1110600
- Porto: 1131200
- Coimbra: 1060300
- Faro: 1080500
- Braga: 1030300
- Aveiro: 1010500
- Évora: 1070500
- Setúbal: 1151200
- Funchal: 2310300
- Ponta Delgada: 3420300

## Exemplos de Chamadas à API

### 1. Obter informações da API

```bash
curl http://localhost:5000/
```

### 2. Listar todos os distritos

```bash
curl http://localhost:5000/distritos
```

### 3. Listar todas as localidades

```bash
curl http://localhost:5000/localidades
```

### 4. Listar localidades de um distrito específico

**Lisboa (ID: 11):**
```bash
curl http://localhost:5000/localidades?distrito_id=11
```

**Porto (ID: 13):**
```bash
curl http://localhost:5000/localidades?distrito_id=13
```

### 5. Obter previsão para uma localidade

**Previsão para Lisboa (5 dias):**
```bash
curl http://localhost:5000/previsao/1110600
```

**Previsão para Porto (3 dias):**
```bash
curl http://localhost:5000/previsao/1131200?dias=3
```

**Previsão para Faro usando query parameters:**
```bash
curl http://localhost:5000/previsao?localidade_id=1080500&dias=5
```

### 6. Formatar a resposta JSON

Para visualizar a resposta de forma mais legível, pode usar `jq` ou `python -m json.tool`:

```bash
curl -s http://localhost:5000/distritos | python3 -m json.tool
```

Ou com jq (se instalado):
```bash
curl -s http://localhost:5000/distritos | jq
```

### 7. Salvar a resposta num ficheiro

```bash
curl -s http://localhost:5000/previsao/1110600 > previsao_lisboa.json
```

### 8. Testar com navegador

Também pode aceder diretamente no navegador:

- http://localhost:5000/
- http://localhost:5000/distritos
- http://localhost:5000/localidades?distrito_id=11
- http://localhost:5000/previsao/1110600

## Exemplos de Respostas

### Resposta de Distritos

```json
{
  "sucesso": true,
  "total": 18,
  "distritos": [
    {
      "id": 1,
      "nome": "Aveiro"
    },
    {
      "id": 2,
      "nome": "Beja"
    }
  ]
}
```

### Resposta de Localidades

```json
{
  "sucesso": true,
  "total": 45,
  "filtro_distrito": 11,
  "localidades": [
    {
      "id": 1110600,
      "nome": "Lisboa",
      "distrito_id": 11,
      "latitude": "38.71",
      "longitude": "-9.14"
    }
  ]
}
```

### Resposta de Previsão

```json
{
  "sucesso": true,
  "dados": {
    "localidade_id": 1110600,
    "total_dias": 5,
    "previsoes": [
      {
        "data": "2025-10-04",
        "temperatura_minima": 15.0,
        "temperatura_maxima": 24.0,
        "probabilidade_precipitacao": 10.0,
        "vento_velocidade": 15.0,
        "vento_direcao": "N",
        "humidade_relativa": 70,
        "id_tempo": 2,
        "descricao_tempo": "Céu pouco nublado"
      }
    ]
  }
}
```

## Tratamento de Erros

### Localidade não encontrada

```bash
curl http://localhost:5000/previsao/999999
```

Resposta:
```json
{
  "erro": "Previsão não encontrada",
  "mensagem": "Não foi possível obter a previsão para a localidade 999999"
}
```

### Parâmetro obrigatório ausente

```bash
curl http://localhost:5000/previsao
```

Resposta:
```json
{
  "erro": "Parâmetro obrigatório ausente",
  "mensagem": "É necessário fornecer o parâmetro localidade_id"
}
```

### Endpoint não encontrado

```bash
curl http://localhost:5000/nao-existe
```

Resposta:
```json
{
  "erro": "Endpoint não encontrado",
  "mensagem": "O recurso solicitado não existe"
}
```

## Integração com Python

### Exemplo de script Python

```python
import requests

# URL base da API
BASE_URL = "http://localhost:5000"

# Obter distritos
response = requests.get(f"{BASE_URL}/distritos")
distritos = response.json()
print(f"Total de distritos: {distritos['total']}")

# Obter previsão para Lisboa
response = requests.get(f"{BASE_URL}/previsao/1110600")
previsao = response.json()

if previsao['sucesso']:
    for dia in previsao['dados']['previsoes']:
        print(f"Data: {dia['data']}")
        print(f"Temperatura: {dia['temperatura_minima']}°C - {dia['temperatura_maxima']}°C")
        print(f"Tempo: {dia['descricao_tempo']}")
        print("---")
```

## Integração com JavaScript

### Exemplo com fetch

```javascript
// Obter previsão para Lisboa
fetch('http://localhost:5000/previsao/1110600')
  .then(response => response.json())
  .then(data => {
    if (data.sucesso) {
      data.dados.previsoes.forEach(dia => {
        console.log(`Data: ${dia.data}`);
        console.log(`Temperatura: ${dia.temperatura_minima}°C - ${dia.temperatura_maxima}°C`);
        console.log(`Tempo: ${dia.descricao_tempo}`);
      });
    }
  })
  .catch(error => console.error('Erro:', error));
```

## Ferramentas de Teste

### Postman

1. Importe a coleção de endpoints
2. Configure a variável `base_url` para `http://localhost:5000`
3. Execute os requests

### HTTPie

```bash
# Instalar HTTPie
pip install httpie

# Usar HTTPie
http GET http://localhost:5000/distritos
http GET http://localhost:5000/previsao/1110600 dias==3
```

## Notas Importantes

- A API utiliza apenas o método GET
- Todas as respostas são em formato JSON
- Os dados são obtidos diretamente da API pública do IPMA
- Algumas localidades podem não ter previsões disponíveis
- O número máximo de dias de previsão depende da disponibilidade do IPMA

