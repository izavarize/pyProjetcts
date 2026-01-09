from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional
import uuid


@dataclass
class Document:
    """
    Representa um documento jurídico original (PDF, HTML, XML).
    """

    document_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    source: str = ""                     # ex: caminho do arquivo ou URL
    doc_type: str = ""                   # pdf | html | xml
    title: Optional[str] = None
    text: str = ""                       # texto normalizado
    metadata: Dict[str, str] = field(default_factory=dict)

    content_hash: str = ""               # SHA-256 do conteúdo normalizado
    created_at: datetime = field(default_factory=datetime.utcnow)
