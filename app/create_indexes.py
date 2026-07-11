from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType

from app.config import settings

client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
)

client.create_payload_index(
    collection_name=settings.QDRANT_COLLECTION,
    field_name="source",
    field_schema=PayloadSchemaType.KEYWORD,
)

client.create_payload_index(
    collection_name=settings.QDRANT_COLLECTION,
    field_name="page",
    field_schema=PayloadSchemaType.INTEGER,
)

print("Indexes created successfully!")