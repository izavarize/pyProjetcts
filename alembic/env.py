from __future__ import annotations

"""
Alembic environment configuration
"""

import sys
import os
from pathlib import Path
from logging.config import fileConfig
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import engine_from_config, pool
from alembic import context

BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"
sys.path.insert(0, str(SRC_DIR))

# =========================
# Alembic Config
# =========================

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)    
# =========================
# Import Base and models
# =========================

#from app.infrastructure.persistence.base import Base  # noqa
try:
    from app.infrastructure.persistence.base import Base
except ModuleNotFoundError as exc:
    raise RuntimeError(
        "Não foi possível importar Base. "
        "Verifique se src/app/infrastructure/persistence/base.py existe "
        "e se todos os diretórios possuem __init__.py"
    ) from exc


from app.infrastructure.persistence import models  # noqa

target_metadata = Base.metadata

# =========================
# Database URL resolution
# =========================

def get_database_url() -> str:
    """
    Alembic MUST rely only on environment variables.
    """
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL environment variable is required for Alembic migrations"
        )
    return url


config.set_main_option(
    "sqlalchemy.url",
    get_database_url()
)

# =========================
# Offline migrations
# =========================

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()

# =========================
# Online migrations
# =========================

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# =========================
# Entrypoint
# =========================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
