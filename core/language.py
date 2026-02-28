"""JARVIS-X Language Detector — O'zbek va Ingliz tili aniqlash tizimi."""


CYRILLIC_RANGE_START = "\u0400"
CYRILLIC_RANGE_END = "\u04ff"

UZ_MARKERS: list[str] = [
    "o'z", "qil", "uchun", "bo'l", "kerak", "nima", "qanday", "salom",
    "rahmat", "menga", "berish", "olish", "yozish", "ochish", "ishla",
    "tushun", "dastur", "loyiha", "vazifa", "men", "bilan", "hamma",
]


class LanguageDetector:
    """Foydalanuvchi matnining tilini aniqlaydigan klass."""

    def detect(self, text: str) -> str:
        """Matn tilini aniqlaydi.

        O'zbek kirill yoki lotin yozuvini, shuningdek o'zbek so'zlarini
        tekshiradi. Ikki yoki undan ko'p marker topilsa "uz" qaytaradi.

        Args:
            text: Tahlil qilinadigan matn.

        Returns:
            "uz" — o'zbek tili, "en" — ingliz tili.
        """
        if not text:
            return "en"

        lower = text.lower()

        # Kirill harflarini tekshirish (o'zbek kirill)
        cyrillic_chars = sum(
            1 for ch in lower if CYRILLIC_RANGE_START <= ch <= CYRILLIC_RANGE_END
        )
        if cyrillic_chars > 2:
            return "uz"

        # O'zbek lotin markerlarini tekshirish
        marker_count = sum(1 for marker in UZ_MARKERS if marker in lower)
        if marker_count >= 2:
            return "uz"

        return "en"

    def get_response_instruction(self, lang: str) -> str:
        """Til asosida javob ko'rsatmasini qaytaradi.

        Args:
            lang: Til kodi ("uz" yoki "en").

        Returns:
            System prompt ga qo'shiladigan ko'rsatma.
        """
        if lang == "uz":
            return "\nRespond entirely in Uzbek language. Use Uzbek for all explanations."
        return "\nRespond in English."
