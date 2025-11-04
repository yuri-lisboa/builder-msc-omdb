# builder-msc-omdb

# 🎬 builder-msc-omdb

> API REST para cadastro e consulta de filmes com integração ao OMDB API, desenvolvida com FastAPI, PostgreSQL e Docker.

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-316192.svg)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Arquitetura](#arquitetura)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [API Endpoints](#api-endpoints)
- [Testes](#testes)
- [Documentação](#documentação)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuindo](#contribuindo)

---

## 🎯 Sobre o Projeto

builder-msc-omdb é um microserviço RESTful desenvolvido para gerenciar um catálogo de filmes. A aplicação busca automaticamente informações detalhadas de filmes na API OMDB e armazena em um banco de dados PostgreSQL, oferecendo endpoints para criação, consulta e listagem de filmes.

## ✨ Funcionalidades

- ✅ **Criar Filme**: Busca dados completos na OMDB API e cadastra no banco
- ✅ **Buscar Filme**: Retorna informações de um filme específico por ID
- ✅ **Listar Filmes**: Lista todos os filmes cadastrados com paginação
- ✅ **Validação**: Impede cadastro de filmes duplicados
- ✅ **Dados Completos**: Título, ano, diretor, atores, sinopse, ratings e mais

---

## 🛠️ Tecnologias

### Backend
- **[Python 3.12](https://www.python.org/)** - Linguagem de programação
- **[FastAPI](https://fastapi.tiangolo.com/)** - Framework web assíncrono
- **[Uvicorn 0.32.1](https://www.uvicorn.org/)** - ASGI server
- **[Pydantic 2.10.3](https://docs.pydantic.dev/)** - Validação de dados

### Database
- **[PostgreSQL](https://www.postgresql.org/)** - Banco de dados relacional
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - ORM assíncrono
- **[asyncpg](https://github.com/MagicStack/asyncpg)** - Driver PostgreSQL assíncrono
- **[Alembic](https://alembic.sqlalchemy.org/)** - Migrations

### HTTP Client
- **[httpx](https://www.python-httpx.org/)** - Cliente HTTP assíncrono para OMDB API

### Testing
- **[pytest](https://docs.pytest.org/)** - Framework de testes
- **[pytest-asyncio](https://pytest-asyncio.readthedocs.io/)** - Suporte async
- **[pytest-cov](https://pytest-cov.readthedocs.io/)** - Coverage

### DevOps
- **[Docker](https://www.docker.com/)** - Containerização
- **[Docker Compose](https://docs.docker.com/compose/)** - Orquestração de containers

---

## 🏗️ Arquitetura

O projeto segue os princípios de **Clean Architecture** com separação clara de responsabilidades:

```
┌─────────────────────────────────────────────────────────┐
│                  Presentation Layer                      │
│              (FastAPI Endpoints - movies.py)             │
│                    HTTP/JSON Interface                   │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                  Business Logic Layer                    │
│                (Service - movie_service.py)              │
│              • Validates business rules                  │
│              • Orchestrates operations                   │
└────────────────────────┬────────────────────────────────┘
                         │
            ┌────────────┴────────────┐
            ▼                         ▼
┌─────────────────────────┐  ┌──────────────────────┐
│    Data Access Layer    │  │   External APIs      │
│   (Repository Pattern)  │  │   (OMDB Client)      │
│  movie_repository.py    │  │  omdb_client.py      │
└─────────┬───────────────┘  └──────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────┐
│              Database Layer (PostgreSQL)                 │
└─────────────────────────────────────────────────────────┘
```


---

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

- **[Docker](https://docs.docker.com/get-docker/)** 
- **[Docker Compose](https://docs.docker.com/compose/install/)**
- **[Git](https://git-scm.com/)**
- **[OMDb API Key](https://www.omdbapi.com/apikey.aspx)**


**OU** para desenvolvimento local sem Docker:

- **[Python 3.12+](https://www.python.org/downloads/)**
- **[PostgreSQL 16+](https://www.postgresql.org/download/)**
- **[OMDb API Key](https://www.omdbapi.com/apikey.aspx)**


---

## 🚀 Instalação

### Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone https://github.com/yuri-lisboa/builder-msc-omdb
cd builder-msc-omdb

# 2. Configure as variáveis de ambiente
cp .env.example .env

# 3. Edite o .env e adicione sua OMDB API key
vim .env  # ou use seu editor preferido

# 4. Inicie os containers
docker-compose up -d

# 5. Verifique se está rodando
docker-compose ps
```

---

## ⚙️ Configuração

### 1. Obter OMDB API Key

A aplicação requer uma chave da API OMDB para buscar informações de filmes:

1. Acesse: **https://www.omdbapi.com/apikey.aspx**
2. Escolha o plano **FREE** (1,000 requisições/dia)
3. Preencha o formulário com seu nome e email
4. Confirme sua conta pelo email recebido
5. Copie a API key fornecida

### 2. Configurar Variáveis de Ambiente

Edite o arquivo `.env` com suas configurações:

```bash
# Database Configuration
POSTGRES_USER=movieuser
POSTGRES_PASSWORD=moviepass
POSTGRES_HOST=db          # Use 'localhost' se rodando local
POSTGRES_PORT=5432
POSTGRES_DB=moviedb

# OMDB API Configuration
OMDB_API_KEY=sua_chave_aqui  # ⚠️ SUBSTITUA pela sua chave real
```

### 3. Verificar Configuração

```bash
# Com Docker
docker-compose logs api

# Local
python -c "from app.core.config import settings; print(settings.OMDB_API_KEY)"
```

⚠️ **IMPORTANTE**: Nunca commite o arquivo `.env` com suas chaves reais! Ele está no `.gitignore` para sua segurança.

---

## 💻 Uso

### Acessar a Aplicação

Após iniciar, a aplicação estará disponível em:

- **API Base**: http://localhost:8000
- **Documentação Interativa (Swagger)**: http://localhost:8000/docs
- **Documentação Alternativa (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### Exemplo Rápido

```bash
# 1. Health Check
curl http://localhost:8000/health

# 2. Criar um filme
curl -X POST "http://localhost:8000/api/v1/movies" \
  -H "Content-Type: application/json" \
  -d '{"title": "The Matrix"}'

# 3. Buscar o filme criado
curl http://localhost:8000/api/v1/movies/1

# 4. Listar todos os filmes
curl http://localhost:8000/api/v1/movies
```

---

## 📡 API Endpoints

### 🎬 Movies

#### POST /api/v1/movies
Cria um novo filme buscando dados na OMDB API.

**Request:**
```json
{
  "title": "Back to the Future"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Back to the Future",
  "year": "1985",
  "rated": "PG",
  "released": "03 Jul 1985",
  "runtime": "116 min",
  "genre": "Adventure, Comedy, Sci-Fi",
  "director": "Robert Zemeckis",
  "writer": "Robert Zemeckis, Bob Gale",
  "actors": "Michael J. Fox, Christopher Lloyd, Lea Thompson",
  "plot": "Marty McFly, a typical American teenager...",
  "language": "English",
  "country": "United States",
  "awards": "Won 1 Oscar. 27 wins & 25 nominations total",
  "imdb_rating": 8.5,
  "imdb_votes": "1,410,143",
  "imdb_id": "tt0088763",
  "box_office": "$214,553,307",
  "created_at": "2024-11-02T12:00:00",
  "updated_at": "2024-11-02T12:00:00"
}
```

**Possíveis Erros:**
- `404 Not Found` - Filme não encontrado na OMDB
- `409 Conflict` - Filme já existe no banco de dados
- `502 Bad Gateway` - Erro ao comunicar com a OMDB API

---

#### GET /api/v1/movies/{id}
Retorna os dados de um filme específico.

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Back to the Future",
  "year": "1985",
  ...
}
```

**Possíveis Erros:**
- `404 Not Found` - Filme não encontrado

---

#### GET /api/v1/movies
Lista todos os filmes cadastrados com paginação.

**Query Parameters:**
- `skip` (opcional): Número de registros a pular (padrão: 0)
- `limit` (opcional): Número máximo de registros (padrão: 100, máximo: 100)

**Exemplo:**
```bash
GET /api/v1/movies?skip=0&limit=10
```

**Response (200 OK):**
```json
{
  "movies": [
    {
      "id": 1,
      "title": "Back to the Future",
      ...
    }
  ],
  "total": 1
}
```

---

### ❤️ Health Check

#### GET /health
Verifica o status da aplicação.

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

---

## 🧪 Testes

O projeto possui uma suíte completa de testes com cobertura >80%.

### Executar Testes

```bash
# Com Docker
docker-compose exec api pytest

# Com cobertura
docker-compose exec api pytest --cov=app --cov-report=html

# Local
pytest
pytest --cov=app --cov-report=html
```


---

### Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🔧 Comandos Úteis

### Docker

```bash
# Iniciar containers
docker-compose up -d

# Parar containers
docker-compose down

# Ver logs
docker-compose logs -f api

# Acessar shell do container
docker-compose exec api bash

# Rebuild containers
docker-compose build
docker-compose up -d

# Remover tudo (incluindo volumes)
docker-compose down -v
```

### Development

```bash
# Formatar código
black .

# Linting
flake8 app tests

# Type checking
mypy app

# Ordenar imports
isort .

# Rodar todos os checks
black . && isort . && flake8 app tests && mypy app
```

### Database

```bash
# Acessar PostgreSQL (Docker)
docker-compose exec db psql -U movieuser -d moviedb

# Ver tabelas
\dt

# Ver dados
SELECT * FROM movies;

# Sair
\q
```

---

## 🐛 Troubleshooting

### Problema: API não inicia

**Solução:**
```bash
# Verificar logs
docker-compose logs api

# Verificar se .env está configurado
cat .env | grep OMDB_API_KEY

# Verificar se PostgreSQL está rodando
docker-compose ps
```

### Problema: "OMDB_API_KEY não configurada"

**Solução:**
```bash
# 1. Verificar se .env existe
ls -la .env

# 2. Verificar conteúdo
cat .env

# 3. Adicionar chave se necessário
echo "OMDB_API_KEY=sua_chave_aqui" >> .env

# 4. Reiniciar containers
docker-compose restart api
```

### Problema: Porta 8000 já em uso

**Solução:**
```bash
# Opção 1: Parar processo usando a porta
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows

# Opção 2: Mudar porta no docker-compose.yml
# Edite: ports: - "8001:8000"
```

### Problema: Database connection error

**Solução:**
```bash
# Aguardar PostgreSQL inicializar (10-20s)
docker-compose logs db

# Verificar se está healthy
docker-compose ps

# Reiniciar API
docker-compose restart api
```

---

## 🚀 Quick Start

```bash
# Setup em 4 comandos
git clone https://github.com/yuri-lisboa/builder-msc-omdb
cd builder-msc-omdb
cp .env.example .env
# Edite .env com sua OMDB_API_KEY
docker-compose up -d

# Testar
curl -X POST "http://localhost:8000/api/v1/movies" \
  -H "Content-Type: application/json" \
  -d '{"title": "The Matrix"}'

# 🎉 Pronto!
```

---

<div align="center">

**[⬆ Voltar ao topo](#-builder-msc-omdb)**

</div>