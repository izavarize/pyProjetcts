Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Bootstrap do ambiente Python - taxSearch " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Verificar Python
try {
    $pythonVersion = python --version
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Error "Python não encontrado. Instale Python 3.11+ antes de continuar."
    exit 1
}

# 2. Criar virtualenv se não existir
if (-not (Test-Path ".venv")) {
    Write-Host "Criando virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
}
else {
    Write-Host ".venv já existe." -ForegroundColor Green
}

# 3. Ativar virtualenv
Write-Host "Ativando virtual environment..." -ForegroundColor Yellow
. .\.venv\Scripts\Activate.ps1

# 4. Atualizar pip
Write-Host "Atualizando pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# 5. Verificar requirements.txt
if (-not (Test-Path "requirements.txt")) {
    Write-Error "Arquivo requirements.txt não encontrado na raiz do projeto."
    exit 1
}

# 6. Instalar dependências
Write-Host "Instalando dependências..." -ForegroundColor Yellow
pip install -r requirements.txt

# 7. Verificação final
Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host " Ambiente configurado com sucesso! " -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para executar o app:" -ForegroundColor Cyan
Write-Host "  python -m app.main" -ForegroundColor White
