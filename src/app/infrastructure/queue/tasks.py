# app/infrastructure/queue/tasks.py
from app.infrastructure.queue.celery_app import celery_app
from app.application.ingestion.full_ingestion_pipeline import FullIngestionPipeline

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=10, retry_kwargs={"max_retries": 3})
def ingest_document_task(self, document_id: str):
    pipeline = FullIngestionPipeline()
    pipeline.run(document_id=document_id)
