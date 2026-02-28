"""JARVIS-X Voice Engine — STT (Kirish) va TTS (Chiqish) tizimi."""

import sys

# Optional STT
try:
    import speech_recognition as sr  # type: ignore[import-untyped]

    STT_AVAILABLE = True
except ImportError:
    STT_AVAILABLE = False

# Optional TTS — pyttsx3 (offline)
try:
    import pyttsx3  # type: ignore[import-untyped]

    TTS_PYTTSX3_AVAILABLE = True
except ImportError:
    TTS_PYTTSX3_AVAILABLE = False

# Optional TTS — gTTS + playsound (online)
try:
    from gtts import gTTS  # type: ignore[import-untyped]
    import playsound  # type: ignore[import-untyped]

    TTS_GTTS_AVAILABLE = True
except ImportError:
    TTS_GTTS_AVAILABLE = False


class VoiceEngine:
    """JARVIS-X ovoz tizimi: mikrofon orqali kirish va ovozli chiqish."""

    LISTEN_TIMEOUT: int = 10
    LISTEN_PHRASE_TIME_LIMIT: int = 30

    def __init__(self) -> None:
        """Mavjud kutubxonalarni tekshiradi, graceful degradation qiladi."""
        self._deps = self._check_dependencies()
        self._tts_engine = None
        if self._deps["pyttsx3"]:
            try:
                self._tts_engine = pyttsx3.init()
            except Exception:
                self._tts_engine = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """Ovoz tizimi ishlayaptimi (kamida STT yoki TTS mavjud).

        Returns:
            True — agar kamida bitta ovoz kutubxonasi mavjud bo'lsa.
        """
        return any(self._deps.values())

    def listen(self) -> str | None:
        """Mikrofondan ovoz oladi va matnga o'giradi.

        Returns:
            Tanilgan matn yoki None (xato bo'lsa).
        """
        if not self._deps["speech_recognition"]:
            print("[VoiceEngine] speech_recognition o'rnatilmagan. Matn rejimi ishlatiladi.")
            return None

        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("🎙️  Gapiring (10 soniya)...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(
                    source,
                    timeout=self.LISTEN_TIMEOUT,
                    phrase_time_limit=self.LISTEN_PHRASE_TIME_LIMIT,
                )
            # Google STT (bepul, internet kerak)
            text = recognizer.recognize_google(audio)
            return str(text)
        except sr.WaitTimeoutError:
            print("[VoiceEngine] Ovoz aniqlanmadi.")
            return None
        except sr.UnknownValueError:
            print("[VoiceEngine] Ovoz tushunilmadi.")
            return None
        except sr.RequestError as exc:
            print(f"[VoiceEngine] STT xizmat xatosi: {exc}")
            return None
        except Exception as exc:
            print(f"[VoiceEngine] Kutilmagan xato: {exc}")
            return None

    def speak(self, text: str) -> None:
        """Matnni ovozga o'giradi va ijro etadi.

        Avval pyttsx3 (offline), keyin gTTS (online), oxirida print.

        Args:
            text: Aytib beriladigan matn.
        """
        if self._tts_engine is not None:
            try:
                self._tts_engine.say(text)
                self._tts_engine.runAndWait()
                return
            except Exception:
                pass

        if self._deps["gtts"]:
            try:
                import tempfile
                import os

                tts = gTTS(text=text, lang="en")
                with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
                    tmp_path = tmp.name
                tts.save(tmp_path)
                playsound.playsound(tmp_path)
                os.unlink(tmp_path)
                return
            except Exception:
                pass

        # Fallback — faqat chop etish
        print(f"[TTS] {text}")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _check_dependencies(self) -> dict[str, bool]:
        """O'rnatilgan ovoz kutubxonalarini tekshiradi.

        Returns:
            Kutubxona nomi → True/False lug'ati.
        """
        return {
            "speech_recognition": STT_AVAILABLE,
            "pyttsx3": TTS_PYTTSX3_AVAILABLE,
            "gtts": TTS_GTTS_AVAILABLE,
        }
