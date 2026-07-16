from qdrant_client import QdrantClient

_client: QdrantClient | None = None


def get_qdrant_client() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(
            host="localhost",
            port=6333,
            timeout=120,
        )
    return _client
