"""Optional voice engine for JARVIS-X.

Provides speech-to-text (STT) and text-to-speech (TTS) capabilities
when the required third-party libraries are available.  If they are not
installed the engine degrades gracefully and reports itself as
unavailable so the rest of the system continues to work in text-only
mode.
"""

from __future__ import annotations

from typing import Optional


class VoiceEngine:
    """Manages STT and TTS for JARVIS-X.

    All voice libraries are imported lazily inside methods so that the
    module can be imported even when those libraries are absent.
    """

    def __init__(self) -> None:
        """Initialise the engine and probe available dependencies."""
        self._deps = self._check_dependencies()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def is_available(self) -> bool:
        """Return *True* when at least STT *and* TTS are both available."""
        return self._deps.get("speech_recognition", False) and (
            self._deps.get("pyttsx3", False) or self._deps.get("gtts", False)
        )

    def listen(self) -> Optional[str]:
        """Capture speech from the microphone and return transcribed text.

        Returns:
            Transcribed string, or *None* when unavailable or on error.
        """
        if not self._deps.get("speech_recognition", False):
            print("[VoiceEngine] SpeechRecognition kutubxonasi o'rnatilmagan.")
            return None

        try:
            import speech_recognition as sr  # type: ignore[import]

            recognizer = sr.Recognizer()
            with sr.Microphone() as source:
                print("[VoiceEngine] Tinglayapman...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=10)
            text: str = recognizer.recognize_google(audio)
            return text
        except Exception as exc:  # noqa: BLE001
            print(f"[VoiceEngine] Ovozni aniqlashda xato: {exc}")
            return None

    def speak(self, text: str) -> None:
        """Convert *text* to speech and play it.

        Prefers *pyttsx3* (offline) and falls back to *gTTS* (online).

        Args:
            text: The text to speak aloud.
        """
        if self._deps.get("pyttsx3", False):
            self._speak_pyttsx3(text)
        elif self._deps.get("gtts", False):
            self._speak_gtts(text)
        else:
            print(f"[VoiceEngine] TTS mavjud emas. Matn: {text}")

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _check_dependencies(self) -> dict[str, bool]:
        """Probe optional voice libraries and return availability map.

        Returns:
            Dict mapping library name to availability boolean.
        """
        deps: dict[str, bool] = {}

        try:
            import speech_recognition  # type: ignore[import]  # noqa: F401
            deps["speech_recognition"] = True
        except ImportError:
            deps["speech_recognition"] = False

        try:
            import pyttsx3  # type: ignore[import]  # noqa: F401
            deps["pyttsx3"] = True
        except ImportError:
            deps["pyttsx3"] = False

        try:
            from gtts import gTTS  # type: ignore[import]  # noqa: F401
            deps["gtts"] = True
        except ImportError:
            deps["gtts"] = False

        return deps

    def _speak_pyttsx3(self, text: str) -> None:
        """Speak using pyttsx3 (offline TTS).

        Args:
            text: Text to synthesise.
        """
        try:
            import pyttsx3  # type: ignore[import]

            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as exc:  # noqa: BLE001
            print(f"[VoiceEngine] pyttsx3 xatosi: {exc}")

    def _speak_gtts(self, text: str) -> None:
        """Speak using gTTS (online TTS, requires internet).

        Args:
            text: Text to synthesise.
        """
        try:
            import tempfile

            from gtts import gTTS  # type: ignore[import]
            import playsound  # type: ignore[import]

            tts = gTTS(text=text, lang="en")
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
                tts.save(tmp.name)
                playsound.playsound(tmp.name)
        except Exception as exc:  # noqa: BLE001
            print(f"[VoiceEngine] gTTS xatosi: {exc}")
