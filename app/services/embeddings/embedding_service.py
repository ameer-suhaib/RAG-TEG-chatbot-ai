from sentence_transformers  import SentenceTransformer
from .embedding_manger import get_embedding_model

class EmbeddingService:
    ## Constructor
    def __init__(self):
        self.model : SentenceTransformer = get_embedding_model()

    ## Single embedding
    def embed(self, text: str) -> list[float]:
        return self.model.encode(
            text,
            normalize_embeddings=True,
        ).tolist()


    ## Multiple embeddings
    def embed_documents(self, texts: list[str]) -> list[list[float]]:

        embeddings = self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True,
            show_progress_bar=False
        )
        return embeddings.tolist()