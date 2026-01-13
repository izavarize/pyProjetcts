/* ============================================================
   taxSearch – Schema completo
   ============================================================ */

-- ============================================================
-- Extensões necessárias
-- ============================================================
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- ============================================================
-- Tabela: documents
-- Representa um documento lógico (ex: CF/88)
-- ============================================================
CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    source TEXT NOT NULL,
    -- Ex: "Constituição Federal", "Lei 8.112/90"

    title TEXT,
    -- Título legível do documento

    current_version TEXT NOT NULL,
    -- Versão ativa (ex: "1988-10-05", "v1")

    metadata JSONB,
    -- Ex: { "jurisdiction": "BR", "type": "constitutional" }

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_documents_source
    ON documents (source);

CREATE INDEX idx_documents_metadata
    ON documents USING gin (metadata);


-- ============================================================
-- Tabela: document_versions
-- Versionamento explícito (jurídico)
-- ============================================================
CREATE TABLE document_versions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    document_id UUID NOT NULL REFERENCES documents(id)
        ON DELETE CASCADE,

    version TEXT NOT NULL,
    -- Ex: "original", "emenda-45", "2024-01"

    effective_date DATE,
    -- Data de vigência (quando aplicável)

    is_active BOOLEAN NOT NULL DEFAULT false,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    UNIQUE (document_id, version)
);

CREATE INDEX idx_document_versions_document
    ON document_versions (document_id);

CREATE INDEX idx_document_versions_active
    ON document_versions (document_id)
    WHERE is_active = true;


-- ============================================================
-- Tabela: document_chunks
-- Chunks semânticos para RAG
-- ============================================================
CREATE TABLE document_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    document_id UUID NOT NULL REFERENCES documents(id)
        ON DELETE CASCADE,

    document_version_id UUID REFERENCES document_versions(id)
        ON DELETE SET NULL,

    content TEXT NOT NULL,
    -- Texto do chunk

    token_count INTEGER NOT NULL,

    embedding VECTOR(768) NOT NULL,
    -- Dimensão compatível com sentence-transformers

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_document_chunks_document
    ON document_chunks (document_id);

CREATE INDEX idx_document_chunks_version
    ON document_chunks (document_version_id);


-- ============================================================
-- Índice vetorial (busca semântica)
-- ============================================================
CREATE INDEX idx_document_chunks_embedding
ON document_chunks
USING hnsw (embedding vector_cosine_ops);


-- ============================================================
-- (Opcional / preparado) Busca textual (FTS)
-- ============================================================
ALTER TABLE document_chunks
ADD COLUMN IF NOT EXISTS search_vector tsvector;

CREATE INDEX idx_document_chunks_search_vector
ON document_chunks
USING gin (search_vector);

-- Atualização manual (quando desejar usar FTS)
-- UPDATE document_chunks
-- SET search_vector = to_tsvector('portuguese', content);


-- ============================================================
-- View auxiliar: chunks ativos (RAG)
-- Facilita queries e debugging
-- ============================================================
CREATE OR REPLACE VIEW v_active_document_chunks AS
SELECT
    dc.id,
    d.source,
    d.title,
    dv.version,
    dc.content,
    dc.token_count,
    dc.embedding,
    dc.created_at
FROM document_chunks dc
JOIN documents d ON d.id = dc.document_id
LEFT JOIN document_versions dv ON dv.id = dc.document_version_id
WHERE dv.is_active = true OR dv.id IS NULL;


-- ============================================================
-- Constraints de integridade adicionais
-- ============================================================
ALTER TABLE document_chunks
ADD CONSTRAINT chk_token_count_positive
CHECK (token_count > 0);
