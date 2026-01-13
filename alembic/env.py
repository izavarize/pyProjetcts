from __future__ import annotations

import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# =========================
# Alembic Config
# =========================

config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# =========================
# Import application settings
# =========================

from app.core.config import settings  # noqa
from app.infrastructure.persistence.base import Base  # noqa

# Import all models so Alembic can see them
from app.infrastructure.persistence import models  # noqa

# =========================
# Metadata
# =========================

target_metadata = Base.metadata


# =========================
# Database URL override
# =========================

def get_database_url() -> str:
    """
    Resolve database URL from environment or settings.
    Priority:
    1. DATABASE_URL env var
    2. settings.database_url
    """
    return os.getenv("DATABASE_URL", settings.database_url)


config.set_main_option(
    "sqlalchemy.url",
    get_database_url()
)


# =========================
# Offline migrations
# =========================

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
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
