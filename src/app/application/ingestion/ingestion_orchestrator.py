# app/application/ingestion/ingestion_orchestrator.py
from app.infrastructure.queue.tasks import ingest_document_task
from app.application.services.document_ingestion_service import DocumentIngestionService

class IngestionOrchestrator:

    def ingest(self, file, metadata: dict) -> str:
        service = DocumentIngestionService()
        document_id = service.register_document(file, metadata)

        ingest_document_task.delay(document_id)

        return document_id
