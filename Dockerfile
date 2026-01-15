#================novo
FROM python:3.12-slim

# =========================
# Sistema
# =========================
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =========================
# Diretório de trabalho
# =========================
WORKDIR /app

# =========================
# Dependências Python
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =========================
# Código
# =========================
#COPY ./src /app/src

ENV PYTHONPATH=/app/src

EXPOSE 8000

#CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]


#===antigo=====
#FROM python:3.12-slim
#
## Evita arquivos .pyc e ativa logs imediatos
#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1
#
#WORKDIR /app
#
## Copia dependências primeiro (camada de cache correta)
#COPY requirements.txt .
#
#RUN pip install --no-cache-dir --upgrade pip \
#    && pip install --no-cache-dir -r requirements.txt
#
## Copia o código da aplicação
#COPY src ./src
#
## Garante que o Python encontre o pacote app
#ENV PYTHONPATH=/app/src
#
## Exposição da porta
#EXPOSE 8000
#
## Comando de inicialização
#CMD ["python", "-m", "uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]


