from sentence_transformers import SentenceTransformer

def get_embedding_model() -> SentenceTransformer:
    """
    """
    return SentenceTransformer(
        "BAAI/bge-m3"
    )