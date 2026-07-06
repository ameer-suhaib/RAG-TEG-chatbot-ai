from .cleaner import ContentCleaner
from .chunker import DocumentChunker
from .language_detector import LanguageDetector
from dotenv import load_dotenv
import os

load_dotenv()

CHUNK_SIZE = os.getenv('CHUNK_SIZE')
print(CHUNK_SIZE,"-------------ccccccccc")
CHUNK_OVERLAP = os.getenv('CHUNK_OVERLAP')

def get_cleaner() -> ContentCleaner:
    """
    Factory for content cleaner.
    """
    return ContentCleaner()


#language detector
def get_language_detector() -> LanguageDetector:
    """
    Factory for language detector.
    """
    return LanguageDetector()

#chunker
def get_chunker() -> DocumentChunker:
    """
    Factory for text chunker.
    """
    return DocumentChunker(chunks_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)