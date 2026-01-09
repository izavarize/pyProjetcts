from sqlalchemy import (
    Column,
    String,
    Integer,
    Text,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector

from app.infrastructure.persistence.db import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    doc_type = Column(String, nullable=False)
    title = Column(String)
    content_hash = Column(String, nullable=False)
    version = Column(Integer, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    chunks = relationship(
        "DocumentChunkModel",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("source", "version", name="uq_document_source_version"),
        UniqueConstraint("content_hash", name="uq_document_hash"),
    )


class DocumentChunkModel(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)

    content = Column(Text, nullable=False)
    source = Column(String, nullable=False)
    token_count = Column(Integer, nullable=False)

    embedding = Column(Vector(384), nullable=False)

    document = relationship("DocumentModel", back_populates="chunks")
