from urllib.parse import urlparse



class LanguageDetector:
    """
    Detects the language of TEG pages.

    Supported:
        en
        ga
    """
    @staticmethod
    def detect(url: str) -> str:
        path = urlparse(url).path.lower()

        if "/ga/" in path:
            return "ga"

        return "en"