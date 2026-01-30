"""hybrid search: add search_vector (FTS) to document_chunks

Revision ID: 0002_hybrid_search_fts
Revises: 0001_initial_schema
Create Date: 2026-01-30

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0002_hybrid_search_fts"
down_revision = "0001_initial_schema"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Garantir extensão para full-text (geralmente já existe)
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # Coluna tsvector para busca full-text em português
    op.add_column(
        "document_chunks",
        sa.Column("search_vector", postgresql.TSVECTOR(), nullable=True),
    )

    # Função que preenche search_vector a partir de content
    op.execute(
        """
        CREATE OR REPLACE FUNCTION document_chunks_search_vector_trigger()
        RETURNS trigger AS $$
        BEGIN
            NEW.search_vector := to_tsvector('portuguese', COALESCE(NEW.content, ''));
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    # Trigger: preenche search_vector em INSERT e UPDATE de content
    op.execute(
        """
        DROP TRIGGER IF EXISTS document_chunks_search_vector_trigger ON document_chunks;
        CREATE TRIGGER document_chunks_search_vector_trigger
        BEFORE INSERT OR UPDATE OF content ON document_chunks
        FOR EACH ROW
        EXECUTE PROCEDURE document_chunks_search_vector_trigger();
        """
    )

    # Backfill: preencher search_vector nos registros já existentes
    op.execute(
        """
        UPDATE document_chunks
        SET search_vector = to_tsvector('portuguese', COALESCE(content, ''))
        WHERE search_vector IS NULL;
        """
    )

    # Índice GIN para busca full-text
    op.create_index(
        "ix_document_chunks_search_vector",
        "document_chunks",
        ["search_vector"],
        postgresql_using="gin",
    )


def downgrade() -> None:
    op.drop_index(
        "ix_document_chunks_search_vector",
        table_name="document_chunks",
        postgresql_using="gin",
    )
    op.execute(
        "DROP TRIGGER IF EXISTS document_chunks_search_vector_trigger ON document_chunks;"
    )
    op.execute("DROP FUNCTION IF EXISTS document_chunks_search_vector_trigger();")
    op.drop_column("document_chunks", "search_vector")
