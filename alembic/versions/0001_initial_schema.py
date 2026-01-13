"""initial schema for taxSearch (documents + RAG)

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-01-09
"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Enable required extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")

    # -------------------------
    # documents
    # -------------------------
    op.create_table(
        "documents",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("version", sa.String(length=50), nullable=False),
        sa.Column("checksum", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("source", "version", name="uq_documents_source_version"),
        sa.UniqueConstraint("checksum", name="uq_documents_checksum"),
    )

    # -------------------------
    # document_chunks
    # -------------------------
    op.create_table(
        "document_chunks",
        sa.Column("id", sa.BigInteger, primary_key=True),
        sa.Column(
            "document_id",
            sa.BigInteger,
            sa.ForeignKey("documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("token_count", sa.Integer, nullable=False),
        sa.Column("embedding", Vector(768), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # -------------------------
    # Indexes
    # -------------------------
    op.create_index(
        "ix_document_chunks_document_id",
        "document_chunks",
        ["document_id"],
    )

    # Vector similarity index (IVFFlat – cosine)
    op.execute(
        """
        CREATE INDEX ix_document_chunks_embedding
        ON document_chunks
        USING ivfflat (embedding vector_cosine_ops)
        WITH (lists = 100);
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_document_chunks_embedding")
    op.drop_index("ix_document_chunks_document_id", table_name="document_chunks")
    op.drop_table("document_chunks")
    op.drop_table("documents")
