# ==========================================================
# taxSearch - Setup Script (Windows / PowerShell)
# ==========================================================
# Responsabilidades:
# - Criar venv
# - Instalar dependências
# - Validar Python
# - Validar PostgreSQL client (psql)
# - Preparar Alembic
# - Rodar migrations
# ==========================================================

Write-Host "== taxSearch :: Setup ==" -ForegroundColor Cyan

# ----------------------------------------------------------
# Verificar Python
# ----------------------------------------------------------
Write-Host "Verificando Python..." -ForegroundColor Yellow

$pythonVersion = python --version 2>$null
if (-not $pythonVersion) {
    Write-Error "Python não encontrado no PATH. Instale Python 3.12+."
    exit 1
}

if ($pythonVersion -notmatch "3\.12") {
    Write-Warning "Versão detectada: $pythonVersion"
    Write-Warning "Recomendado Python 3.12.x"
}

# ----------------------------------------------------------
# Criar venv
# ----------------------------------------------------------
if (-not (Test-Path ".venv")) {
    Write-Host "Criando virtualenv (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
} else {
    Write-Host "Virtualenv já existe." -ForegroundColor Green
}

# ----------------------------------------------------------
# Ativar venv
# ----------------------------------------------------------
Write-Host "Ativando virtualenv..." -ForegroundColor Yellow
. .\.venv\Scripts\Activate.ps1

# ----------------------------------------------------------
# Atualizar pip
# ----------------------------------------------------------
Write-Host "Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# ----------------------------------------------------------
# Instalar dependências
# ----------------------------------------------------------
if (-not (Test-Path "requirements.txt")) {
    Write-Error "Arquivo requirements.txt não encontrado."
    exit 1
}

Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# ----------------------------------------------------------
# Validar dependências críticas
# ----------------------------------------------------------
Write-Host "Validando dependências críticas..." -ForegroundColor Yellow

$requiredModules = @(
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "alembic",
    "psycopg",
    "pgvector",
    "google.genai",
    "sentence_transformers"
)

foreach ($module in $requiredModules) {
    python - << EOF
import importlib, sys
try:
    importlib.import_module("$module")
except Exception as e:
    print("ERRO: módulo ausente -> $module")
    sys.exit(1)
EOF

    if ($LASTEXITCODE -ne 0) {
        Write-Error "Falha ao importar $module"
        exit 1
    }
}

Write-Host "Dependências OK." -ForegroundColor Green

# ----------------------------------------------------------
# Verificar .env
# ----------------------------------------------------------
if (-not (Test-Path ".env")) {
    Write-Warning ".env não encontrado. Criando .env de exemplo..."
@"
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/taxsearch
GEMINI_API_KEY=CHANGE_ME
ENV=local
"@ | Out-File .env -Encoding utf8
}

# ----------------------------------------------------------
# Alembic
# ----------------------------------------------------------
if (-not (Test-Path "alembic.ini")) {
    Write-Error "alembic.ini não encontrado."
    exit 1
}

Write-Host "Executando Alembic upgrade..." -ForegroundColor Yellow
alembic upgrade head

if ($LASTEXITCODE -ne 0) {
    Write-Error "Erro ao executar Alembic."
    exit 1
}

# ----------------------------------------------------------
# Final
# ----------------------------------------------------------
Write-Host ""
Write-Host "Setup concluído com sucesso." -ForegroundColor Green
Write-Host ""
Write-Host "Próximos passos:" -ForegroundColor Cyan
Write-Host "1) docker compose up -d  (opcional)"
Write-Host "2) python -m app.main"
Write-Host "3) uvicorn app.api.main:app --reload"
Write-Host ""
