#!/usr/bin/env bash

set -e

PROJECT_ROOT="d:/isaac/prjtest/taxSearch"

# Diretórios
mkdir -p \
  $PROJECT_ROOT/src/app/core \
  $PROJECT_ROOT/src/app/domain \
  $PROJECT_ROOT/src/app/application \
  $PROJECT_ROOT/src/app/infrastructure/ai \
  $PROJECT_ROOT/tests

# Arquivos Python (__init__.py)
touch \
  $PROJECT_ROOT/src/app/__init__.py \
  $PROJECT_ROOT/src/app/core/__init__.py \
  $PROJECT_ROOT/src/app/domain/__init__.py \
  $PROJECT_ROOT/src/app/application/__init__.py \
  $PROJECT_ROOT/src/app/infrastructure/__init__.py \
  $PROJECT_ROOT/src/app/infrastructure/ai/__init__.py \
  $PROJECT_ROOT/tests/__init__.py

# Arquivos de código
touch \
  $PROJECT_ROOT/src/app/core/config.py \
  $PROJECT_ROOT/src/app/core/logging.py \
  $PROJECT_ROOT/src/app/core/exceptions.py \
  $PROJECT_ROOT/src/app/domain/models.py \
  $PROJECT_ROOT/src/app/application/services.py \
  $PROJECT_ROOT/src/app/infrastructure/ai/llm_client.py \
  $PROJECT_ROOT/src/app/main.py

# Arquivos de projeto
touch \
  $PROJECT_ROOT/.gitignore \
  $PROJECT_ROOT/pyproject.toml \
  $PROJECT_ROOT/README.md \
  $PROJECT_ROOT/.env.example

echo "Estrutura de projeto criada com sucesso em ./$PROJECT_ROOT"
