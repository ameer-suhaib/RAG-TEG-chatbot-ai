"""
remove excessive blank lines
normalize whitespace
remove tabs
strip invisible characters
"""

import re
import unicodedata

class ContentCleaner:
    """
    Cleans markdown produced by Crawl4AI.
    """
    @staticmethod
    def clean(markdown: str) -> str:
        if not markdown:
            return ""

        #unicode notmaliazation
        markdown = unicodedata.normalize("NFKC", markdown)

        # Convert tabs
        markdown = markdown.replace("\t", " ")

        # Remove trailing spaces
        markdown = re.sub(r"[ \t]+$", "", markdown, flags=re.MULTILINE)

        # Collapse excessive blank lines
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        # Collapse multiple spaces
        markdown = re.sub(r"[ ]{2,}", " ", markdown)
        
        # Remove zero-width characters
        markdown = re.sub(
            r"[\u200B-\u200D\uFEFF]",
            "",
            markdown,
        )

        return markdown.strip()


