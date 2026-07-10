from qdrant_client import models
from .qdrant_manager import get_qdrant_client
from app.services.processing.models import ProcessedChunk

class QdrantService:
    def __init__(self):
        self.collection = "teg_documents"
        self.client = get_qdrant_client()


    def create_collection(self):
        if self.client.collection_exists(self.collection):
            return 

        ## 1024 is because ,BAAI/bge-m3
        self.client.create_collection(
            collection_name=self.collection,
            vectors_config=models.VectorParams(size = 1024, distance = models.Distance.COSINE)
        )


    def upsert_chunks(
        self,
        chunks: list[ProcessedChunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Stores processed chunks and their embeddings in Qdrant.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "Number of chunks and embeddings must match."
            )

        points: list[models.PointStruct] = []

        for chunk, embedding in zip(chunks, embeddings):

            payload = {
                "chunk_id": chunk.chunk_id,
                "content": chunk.content,
                "url": str(chunk.url),
                "title": chunk.title,
                "language": chunk.language,
                "chunk_index": chunk.chunk_index,
                "crawled_at": chunk.crawled_at.isoformat(),
            }

            points.append(
                models.PointStruct(
                    id=chunk.chunk_id,
                    vector=embedding,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection,
            wait=True,
            points=points,
        )

    
    def search(self, query_vector : list[float], language: str, limit : int = 5, score_threshold : float = 0.35):
        return self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="language",
                        match=models.MatchValue(value=language) #filtering by language
                    )
                ]
            )
        )
    