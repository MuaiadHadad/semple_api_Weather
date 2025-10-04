# API de Previsão Meteorológica - IPMA

REST API desenvolvida em Python para consultar previsões meteorológicas do Instituto Português do Mar e da Atmosfera (IPMA).

## Descrição

Aplicação que permite consultar previsões meteorológicas para qualquer localidade em Portugal através de uma API RESTful simples. Os dados são obtidos em tempo real da API pública do IPMA.

**Inclui interface web para testes (sem necessidade de Postman)!**

## Características

- Consulta de previsões por localidade e distrito
- Parâmetros dinâmicos via API (sem alterar código)
- Interface web interativa para testes
- Suporte completo para Docker
- API REST com CORS habilitado

## Tecnologias

- Python 3.9
- Flask (Framework web)
- Flask-CORS (Suporte CORS)
- Requests (Comunicação HTTP)
- Gunicorn (Servidor produção)
- Docker & Docker Compose

## Instalação Rápida

### Com Docker (Recomendado)

```bash
git clone https://github.com/seu-usuario/semple_api_Weather.git
cd semple_api_Weather
docker-compose up -d
```

Acesse: http://localhost:5000

### Sem Docker

```bash
git clone https://github.com/seu-usuario/semple_api_Weather.git
cd semple_api_Weather
./install.sh
./run.sh
```

## Como Usar

### Interface Web (Recomendado)

Abra no navegador: **http://localhost:5000/index.html**

A interface permite:
- Listar todos os distritos de Portugal
- Filtrar localidades por distrito
- Consultar previsões meteorológicas
- Testar todos os endpoints sem Postman

### API Endpoints

#### 1. Listar Distritos
```bash
GET http://localhost:5000/distritos
```

**Exemplo:**
```bash
curl http://localhost:5000/distritos
```

**Resposta:**
```json
{
  "sucesso": true,
  "total": 29,
  "distritos": [
    {"id": 1, "nome": "Aveiro"},
    {"id": 11, "nome": "Lisboa"},
    {"id": 13, "nome": "Porto"}
  ]
}
```

#### 2. Listar Localidades
```bash
GET http://localhost:5000/localidades
GET http://localhost:5000/localidades?distrito_id=11
```

**Exemplos:**
```bash
# Todas as localidades
curl http://localhost:5000/localidades

# Apenas Lisboa
curl http://localhost:5000/localidades?distrito_id=11
```

**Resposta:**
```json
{
  "sucesso": true,
  "total": 45,
  "localidades": [
    {
      "id": 1110600,
      "nome": "Lisboa",
      "distrito_id": 11,
      "distrito_nome": "Lisboa",
      "latitude": "38.71",
      "longitude": "-9.14"
    }
  ]
}
```

#### 3. Consultar Previsão
```bash
GET http://localhost:5000/previsao/{localidade_id}
GET http://localhost:5000/previsao/{localidade_id}?dias=3
```

**Exemplos:**
```bash
# Previsão para Lisboa (5 dias)
curl http://localhost:5000/previsao/1110600

# Previsão para Porto (3 dias)
curl http://localhost:5000/previsao/1131200?dias=3
```

**Resposta:**
```json
{
  "sucesso": true,
  "dados": {
    "localidade_id": 1110600,
    "total_dias": 3,
    "previsoes": [
      {
        "data": "2025-10-04",
        "temperatura_minima": 15.0,
        "temperatura_maxima": 24.0,
        "probabilidade_precipitacao": 10.0,
        "vento_velocidade": 15.0,
        "vento_direcao": "N",
        "humidade_relativa": 70,
        "descricao_tempo": "Céu pouco nublado"
      }
    ]
  }
}
```

## IDs das Cidades Principais

| Cidade | ID | Distrito |
|--------|-----|----------|
| Lisboa | 1110600 | 11 |
| Porto | 1131200 | 13 |
| Coimbra | 1060300 | 6 |
| Faro | 1080500 | 8 |
| Braga | 1030300 | 3 |
| Aveiro | 1010500 | 1 |

**Dica:** Use a interface web ou endpoint `/localidades` para encontrar IDs de outras cidades.

## Estrutura do Projeto

```
semple_api_Weather/
├── app.py                  # API Flask principal
├── config.py               # Configurações
├── index.html              # Interface web de testes
├── services/
│   └── ipma_service.py    # Serviço IPMA
├── requirements.txt        # Dependências Python
├── Dockerfile              # Imagem Docker
├── docker-compose.yml      # Orquestração
├── install.sh              # Script instalação
└── run.sh                  # Script execução
```

## Comandos Docker

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar
docker-compose down

# Reconstruir
docker-compose up -d --build
```

## Tratamento de Erros

A API retorna erros em JSON com códigos HTTP apropriados:

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Parâmetros inválidos |
| 404 | Recurso não encontrado |
| 500 | Erro interno |
| 503 | Serviço indisponível |

**Exemplo de erro:**
```json
{
  "erro": "Previsão não encontrada",
  "mensagem": "Não foi possível obter a previsão para a localidade 999999"
}
```

## Testando a API

### 1. Interface Web (Mais fácil)
Abra: http://localhost:5000/index.html

### 2. cURL (Terminal)
```bash
curl http://localhost:5000/distritos
curl http://localhost:5000/previsao/1110600
```

### 3. Navegador
Acesse diretamente:
- http://localhost:5000/distritos
- http://localhost:5000/localidades?distrito_id=11
- http://localhost:5000/previsao/1110600

### 4. Postman/Insomnia
Importe os endpoints e teste conforme necessário.

## Deploy em Produção

### Docker (Recomendado)
```bash
docker-compose up -d
```

### Servidor tradicional
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Configuração

Edite o ficheiro `.env`:
```env
FLASK_APP=app.py
FLASK_ENV=production
PORT=5000
```

## Requisitos do Exercício

✅ Recolhe dados da API do IPMA  
✅ REST API funcional com 4 endpoints  
✅ Parâmetros dinâmicos (distrito/localidade via API)  
✅ Estrutura organizada e bem documentada  
✅ Disponível no GitHub  
✅ **BÓNUS:** Docker completo  
✅ **EXTRA:** Interface web para testes sem Postman  

## Resolução de Problemas

**Porta 5000 em uso:**
```bash
# Edite .env e mude a porta
PORT=8000
```

**Docker não inicia:**
```bash
docker-compose down
docker-compose up -d --build
```

**CORS Error no frontend:**
Certifique-se que a API está rodando em http://localhost:5000

## Licença

Código aberto - disponível para uso educacional e comercial.

## Autor

Desenvolvido como projeto de demonstração de REST API com integração de dados externos.
