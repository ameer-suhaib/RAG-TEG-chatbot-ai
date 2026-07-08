from lingua import Language, LanguageDetectorBuilder



class LanguageDetector:
    """
    Detects the language of TEG pages.

    Supported:
        en
        ga
    """
    @staticmethod
    def detect(cleaned_text: str) -> str:
        detector = LanguageDetectorBuilder.from_languages(
            Language.ENGLISH,
            Language.IRISH
        ).build()

        language = detector.detect_language_of(cleaned_text)
        if language.name == 'IRISH':
            return "ga"
        return "en"