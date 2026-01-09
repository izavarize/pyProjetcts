from dataclasses import dataclass, field
from typing import Dict
import uuid


@dataclass
class DocumentChunk:
    """
    Representa um fragmento de documento usado no RAG.
    """

    chunk_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    document_id: str = ""                # vínculo com Document
    content: str = ""                    # texto do chunk
    source: str = ""                     # fonte original
    metadata: Dict[str, str] = field(default_factory=dict)

    token_count: int = 0                 # controle de tamanho
