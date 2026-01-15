/* ============================================================================
   Projeto: taxSearch
   Arquivo: postgres/init.sql
   Objetivo:
     - Inicializar extensões obrigatórias
     - Criar schemas base
     - Criar tabelas RAG fundamentais
     - Preparar índices vetoriais (pgvector)
     - Garantir consistência para Alembic
   ============================================================================ */

-- ============================================================================
-- Extensões obrigatórias
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ============================================================================
-- Schema lógico do projeto
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS rag;
SET search_path TO rag, public;

-- ============================================================================
-- Tabela: documents
-- Metadados dos documentos jurídicos
-- ============================================================================

CREATE TABLE IF NOT EXISTS documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source TEXT NOT NULL,
    version TEXT NOT NULL,
    description TEXT,
    document_type TEXT NOT NULL,        -- ex: 'CF', 'Lei', 'Decreto'
    published_at DATE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_documents_source
    ON documents (source);

CREATE INDEX IF NOT EXISTS idx_documents_type
    ON documents (document_type);

-- ============================================================================
-- Tabela: document_chunks
-- Fragmentos semânticos com embeddings
-- ============================================================================

CREATE TABLE IF NOT EXISTS document_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    document_id UUID NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER NOT NULL,
    embedding VECTOR(1536) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_chunks_document
    ON document_chunks (document_id);

-- Índice vetorial (cosine distance)
CREATE INDEX IF NOT EXISTS idx_chunks_embedding
    ON document_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- ============================================================================
-- View auxiliar para depuração e auditoria
-- ============================================================================

CREATE OR REPLACE VIEW v_document_chunks_audit AS
SELECT
    d.source,
    d.version,
    d.document_type,
    dc.chunk_index,
    dc.token_count,
    length(dc.content) AS content_length,
    dc.created_at
FROM document_chunks dc
JOIN documents d ON d.id = dc.document_id;

-- ============================================================================
-- Função de sanity check do banco RAG
-- ============================================================================

CREATE OR REPLACE FUNCTION rag_health_check()
RETURNS TABLE (
    check_name TEXT,
    status TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT 'pgvector_extension', 
           CASE WHEN EXISTS (
               SELECT 1 FROM pg_extension WHERE extname = 'vector'
           ) THEN 'OK' ELSE 'MISSING' END;

    RETURN QUERY
    SELECT 'documents_table',
           CASE WHEN EXISTS (
               SELECT 1 FROM information_schema.tables
               WHERE table_schema = 'rag'
                 AND table_name = 'documents'
           ) THEN 'OK' ELSE 'MISSING' END;

    RETURN QUERY
    SELECT 'document_chunks_table',
           CASE WHEN EXISTS (
               SELECT 1 FROM information_schema.tables
               WHERE table_schema = 'rag'
                 AND table_name = 'document_chunks'
           ) THEN 'OK' ELSE 'MISSING' END;

    RETURN QUERY
    SELECT 'embedding_dimension',
           CASE WHEN EXISTS (
               SELECT 1
               FROM information_schema.columns
               WHERE table_schema = 'rag'
                 AND table_name = 'document_chunks'
                 AND column_name = 'embedding'
           ) THEN 'OK' ELSE 'INVALID' END;
END;
$$;

-- ============================================================================
-- Comentários finais
-- ============================================================================

COMMENT ON SCHEMA rag IS 'Schema principal do RAG jurídico (taxSearch)';
COMMENT ON TABLE documents IS 'Metadados de documentos jurídicos';
COMMENT ON TABLE document_chunks IS 'Fragmentos semânticos com embeddings vetoriais';

-- Fim do script
