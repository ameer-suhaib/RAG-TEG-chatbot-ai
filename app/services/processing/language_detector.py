from lingua import Language, LanguageDetectorBuilder

_detector = None


def _get_detector():
    global _detector
    if _detector is None:
        _detector = LanguageDetectorBuilder.from_languages(
            Language.ENGLISH,
            Language.IRISH,
        ).build()
    return _detector


class LanguageDetector:
    """
    Detects the language of TEG pages.

    Supported:
        en
        ga
    """

    def detect(self, cleaned_text: str) -> str:
        language = _get_detector().detect_language_of(cleaned_text)
        if language and language.name == "IRISH":
            return "ga"
        return "en"
