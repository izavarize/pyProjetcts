# TaxSearch - Plataforma RAG Jurídico-Fiscal

Sistema avançado de busca e resposta baseado em RAG (Retrieval-Augmented Generation) para consultas jurídico-fiscais. Utiliza PostgreSQL com extensão pgvector para busca vetorial, Google Gemini para geração de respostas e embeddings locais para processamento de documentos.

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [API](#api)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Docker](#docker)

## 🚀 Funcionalidades

### Sistema RAG Completo

- **Busca Híbrida**: Vetor (pgvector, 384 dim) + full-text (tsvector, português) com pesos configuráveis
- **Chunking Jurídico**: Sistema híbrido de chunking que prioriza estrutura legal (artigos, parágrafos)
- **Geração de Respostas**: Integração com Google Gemini para respostas contextualizadas
- **Citações Explícitas**: Respostas incluem fontes e scores de relevância

### Ingestão de Documentos

- **Múltiplos Formatos**: Suporte a PDF, HTML, XML
- **Normalização**: Normalização de texto jurídico com preservação de estrutura
- **Deduplicação**: Sistema de versionamento e deduplicação de documentos
- **Pipeline Completo**: Pipeline automatizado de ingestão

### API REST

- **FastAPI**: API moderna e rápida
- **Rate Limiting**: Controle de taxa de requisições
- **Cache**: Cache em memória para respostas frequentes
- **Health Checks**: Endpoints de monitoramento

### Observabilidade

- **Telemetria**: Sistema de coleta de métricas
- **Logging**: Logging estruturado com Loguru
- **Métricas**: Endpoints de métricas para monitoramento

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas bem definida:

```
taxSearch/
├── src/app/
│   ├── api/                    # Camada de API
│   │   ├── routers/           # Endpoints REST
│   │   ├── schemas/           # Modelos Pydantic
│   │   ├── middleware/        # Middlewares (rate limit)
│   │   └── deps.py            # Dependências FastAPI
│   ├── application/            # Camada de aplicação
│   │   ├── rag/               # Serviços RAG
│   │   ├── ingestion/         # Orquestração de ingestão
│   │   ├── chunking/          # Chunking jurídico
│   │   └── ai_service.py       # Serviço de IA
│   ├── infrastructure/         # Camada de infraestrutura
│   │   ├── ai/                # Clientes de IA (Gemini)
│   │   ├── rag/               # Implementações RAG
│   │   ├── persistence/       # Repositórios e modelos
│   │   ├── ingest/            # Loaders de documentos
│   │   ├── embeddings/        # Geradores de embeddings
│   │   └── observability/     # Telemetria
│   ├── domain/                 # Modelos de domínio
│   │   ├── document.py
│   │   ├── document_chunk.py
│   │   └── rag_response.py
│   └── core/                   # Configuração e infraestrutura base
│       ├── config.py
│       ├── database.py
│       └── logging.py
```

### Componentes Principais

#### Camada de API

- **Routers**:
  - `/ask`: Endpoint principal para consultas RAG
  - `/health`: Health check
  - `/ingestion`: Endpoints de ingestão de documentos
  - `/metrics`: Métricas do sistema

- **Middleware**:
  - Rate limiting configurável (padrão: 20 req/min)
  - Cache em memória com TTL

#### Camada de Aplicação

- **RAGAnswerService**: Orquestra o fluxo completo RAG
  - Geração de embeddings da query
  - Busca vetorial
  - Construção de prompt contextualizado
  - Geração de resposta com Gemini

- **RAGRetriever**: Busca vetorial
  - Integração com pgvector
  - Filtro por score mínimo
  - Ordenação por relevância

- **RAGPromptBuilder**: Construção de prompts
  - Injeção de contexto
  - Formatação de evidências
  - Instruções para citação

- **JuridicalChunker**: Chunking especializado
  - Divisão por artigos/parágrafos
  - Fallback para tokenização
  - Overlap configurável
  - Preservação de metadados jurídicos

- **FullIngestionPipeline**: Pipeline completo de ingestão
  - Carregamento de documentos
  - Normalização
  - Chunking
  - Geração de embeddings
  - Persistência versionada

#### Camada de Infraestrutura

- **GeminiClient**: Cliente para Google Gemini
  - Suporte a múltiplos modelos
  - Tratamento de erros
  - Retry logic

- **LocalEmbedder**: Geração de embeddings locais
  - Sentence Transformers
  - Dimensão fixa: 384 (compatível com pgvector)
  - Batch processing

- **PGVectorRetriever**: Busca vetorial nativa
  - SQL direto com operador `<=>` (distância cosseno)
  - Índice HNSW para performance
  - Filtro por score mínimo

- **Document Loaders**:
  - `PDFLoader`: Extração de texto de PDFs
  - `HTMLLoader`: Parsing de HTML
  - `XMLLoader`: Parsing de XML

- **TextNormalizer**: Normalização de texto jurídico
  - Preservação de estrutura (artigos, parágrafos)
  - Normalização de espaços e caracteres
  - Divisão por artigos

#### Persistência

- **Models**: SQLAlchemy ORM
  - `DocumentChunk`: Chunks com embeddings
  - Índices HNSW para busca vetorial
  - Índices GIN para busca full-text (TSVECTOR)

- **Repositories**: Abstração de acesso a dados
  - Versionamento de documentos
  - Deduplicação
  - Queries otimizadas

## 🛠️ Tecnologias

### Core

- **Python 3.12+**: Linguagem principal
- **FastAPI**: Framework web moderno
- **SQLAlchemy 2.0**: ORM
- **Alembic**: Migrações de banco de dados

### Banco de Dados

- **PostgreSQL 16**: Banco de dados principal
- **pgvector**: Extensão para busca vetorial
- **HNSW Index**: Índice para busca vetorial otimizada

### IA e NLP

- **Google Gemini**: Modelo de linguagem para geração
- **Sentence Transformers**: Geração de embeddings locais
- **scikit-learn**: Utilitários de NLP

### Documentos

- **pypdf**: Extração de PDF
- **python-docx**: Processamento de Word
- **BeautifulSoup4**: Parsing HTML/XML
- **lxml**: Parser XML rápido

### Observabilidade

- **Loguru**: Logging estruturado
- **Telemetria Custom**: Sistema de métricas

## 📦 Instalação

### Pré-requisitos

- Python 3.12 ou superior
- PostgreSQL 16 com extensão pgvector
- Docker e Docker Compose (recomendado)

### Instalação Local

```bash
# Clonar repositório
cd prjtest/taxSearch

# Instalar dependências
pip install -e .

# Ou com pip diretamente
pip install -r requirements.txt
```

### Configuração do Banco de Dados

```bash
# Criar banco de dados
createdb ragdb

# Instalar extensão pgvector
psql ragdb -c "CREATE EXTENSION vector;"

# Executar migrações
alembic upgrade head
```

### Variáveis de Ambiente

Crie um arquivo `.env`:

```env
# Gemini
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Database
PG_DSN=postgresql://postgres:postgres@localhost:5432/ragdb

# App
ENV=local
LOG_LEVEL=INFO

# RAG
MIN_SCORE=0.75
# Híbrido (vetor + full-text): alpha (vetor) + beta (full-text)
RAG_HYBRID_ALPHA=0.7
RAG_HYBRID_BETA=0.3
```

## ⚙️ Configuração

### Configurações Principais

As configurações são carregadas via Pydantic Settings:

- **GEMINI_API_KEY**: Chave da API do Google Gemini (obrigatório)
- **GEMINI_MODEL**: Modelo a usar (padrão: `gemini-2.5-flash`)
- **PG_DSN**: String de conexão PostgreSQL (obrigatório)
- **MIN_SCORE**: Score mínimo para retornar chunks (padrão: 0.75)
- **RAG_HYBRID_ALPHA**: Peso da busca vetorial no híbrido (padrão: 0.7)
- **RAG_HYBRID_BETA**: Peso da busca full-text no híbrido (padrão: 0.3)
- **LOG_LEVEL**: Nível de log (padrão: INFO)

### Configuração de Chunking

O `JuridicalChunker` aceita:

- `max_tokens`: Tamanho máximo do chunk (padrão: 400)
- `overlap`: Overlap entre chunks (padrão: 50)

### Configuração de Rate Limiting

No `RateLimitMiddleware`:

- `max_requests`: Máximo de requisições (padrão: 20)
- `window_seconds`: Janela de tempo (padrão: 60)

## 🎯 Uso

### Executar API

```bash
# Com uvicorn
uvicorn app.api.main:app --reload --port 8000

# Ou via script
python -m app.main
```

### Ingestão de Documentos

```python
from app.application.ingestion.full_ingestion_pipeline import FullIngestionPipeline
from pathlib import Path

pipeline = FullIngestionPipeline()

# Ingerir diretório
pipeline.ingest(directory=Path("data/documents"))

# Ou arquivos específicos
pipeline.ingest(files=[Path("data/cf88.txt")])
```

### Scripts de Ingestão

```bash
# Ingestão de CF88
python scripts/seed_cf88.py

# Validação do banco
python scripts/validate_database.py

# Ingestão genérica
python scripts/run_ingestion.py --path data/documents
```

## 🌐 API

### Endpoints

#### POST `/ask`

Realiza uma consulta RAG.

**Request:**
```json
{
  "question": "O que dispõe o art. 3º da Constituição Federal?"
}
```

**Response:**
```json
{
  "answer": "O art. 3º da Constituição Federal estabelece...",
  "sources": [
    {
      "source": "CF88",
      "score": 0.892
    }
  ],
  "used_rag": true
}
```

#### GET `/health`

Health check do sistema.

**Response:**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

#### POST `/ingestion`

Ingere documentos no sistema.

**Request:**
```json
{
  "source": "CF88",
  "doc_type": "legislacao",
  "files": ["path/to/document.pdf"]
}
```

### Cache

O endpoint `/ask` utiliza cache em memória:
- TTL: 300 segundos (5 minutos)
- Chave: Hash SHA-256 da pergunta normalizada
- Apenas respostas com RAG são cacheadas

## 📁 Estrutura do Projeto

```
taxSearch/
├── src/app/
│   ├── api/                    # API REST
│   ├── application/            # Lógica de aplicação
│   ├── infrastructure/         # Implementações técnicas
│   ├── domain/                 # Modelos de domínio
│   └── core/                   # Configuração base
├── alembic/                     # Migrações
│   └── versions/
├── scripts/                     # Scripts utilitários
│   ├── seed_cf88.py
│   └── run_ingestion.py
├── tests/                       # Testes
│   ├── test_chunking_juridical.py
│   └── test_rag_integrity.py
├── docker/                      # Configurações Docker
│   └── grafana/
├── postgres/                    # Scripts SQL
│   └── init.sql
├── pyproject.toml              # Configuração do projeto
├── requirements.txt            # Dependências
├── Dockerfile                  # Container da API
└── docker-compose.yml          # Orquestração
```

## 🐳 Docker

### Execução com Docker Compose

```bash
# Iniciar serviços
docker-compose up -d

# Ver logs
docker-compose logs -f api

# Parar serviços
docker-compose down
```

### Serviços

- **postgres**: PostgreSQL 16 com pgvector
  - Porta: 5432
  - Volume persistente: `pgdata`

- **api**: API FastAPI
  - Porta: 8000
  - Hot reload habilitado (volume montado)

### Inicialização do Banco

O script `postgres/init.sql` é executado automaticamente na primeira inicialização, criando:
- Extensão pgvector
- Estrutura de tabelas básica

## 🔍 Detalhes Técnicos

### Busca Híbrida (vetor + full-text)

O RAG usa combinação ponderada de:

- **Vetor**: similaridade por cosseno no pgvector (embedding da pergunta × embedding do chunk).
- **Full-text**: `ts_rank_cd` em `search_vector` (tsvector em português) com `plainto_tsquery`.

Fórmula: `score = alpha * vector_score + beta * fts_score` (padrão alpha=0.7, beta=0.3). O `search_vector` é preenchido por trigger a partir de `content` e por backfill na migration `0002_hybrid_search_fts`.

### Busca Vetorial

O sistema utiliza pgvector com:

- **Dimensão**: 384 (compatível com Sentence Transformers)
- **Índice**: HNSW (Hierarchical Navigable Small World)
  - `m`: 16 (conexões por nó)
  - `ef_construction`: 64 (precisão na construção)
- **Operador**: `<=>` (distância cosseno)
- **Score**: `1 - distancia` (maior = mais relevante)

### Chunking Jurídico

Estratégia híbrida:

1. **Divisão por Artigos**: Prioriza estrutura legal
2. **Tokenização**: Fallback quando artigo excede limite
3. **Overlap**: Preserva contexto entre chunks
4. **Metadados**: Captura artigo/parágrafo quando possível

### Embeddings

- **Modelo**: Sentence Transformers (local)
- **Dimensão**: 384
- **Batch Processing**: Processamento em lote para performance
- **Normalização**: Texto normalizado antes de embedding

### Versionamento de Documentos

Sistema de versionamento permite:
- Atualização de documentos existentes
- Histórico de versões
- Deduplicação inteligente

### Observabilidade

- **Telemetria**: Coleta de métricas de uso
- **Logging Estruturado**: Logs com contexto
- **Métricas**: Endpoints para Prometheus/Grafana

## 🧪 Testes

```bash
# Executar testes
pytest

# Com cobertura
pytest --cov=app tests/

# Testes específicos
pytest tests/test_chunking_juridical.py
```

### Testes Disponíveis

- `test_chunking_juridical.py`: Testes de chunking jurídico
- `test_rag_integrity.py`: Testes de integridade RAG
- `test_retriever_scores.py`: Testes de scores de busca

## 📝 Notas

- O sistema requer chave de API do Google Gemini
- A primeira ingestão pode levar tempo dependendo do volume de documentos
- O cache melhora significativamente a performance para consultas repetidas
- O rate limiting protege contra abuso da API

## 🔐 Segurança

- Rate limiting implementado
- Validação de entrada com Pydantic
- Sanitização de queries
- Isolamento de erros (não expõe detalhes internos)

## 👤 Autor

Isaac Evangelista - izavarize@gmail.com

## 📄 Licença

Proprietary
