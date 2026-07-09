import subprocess
import time
import threading

LANGUAGES = {
    "english": "en",
    "telugu": "te",
    "hindi": "hi",
    "marathi": "mr",
    "gujarati": "gu",
    "tamil": "ta",
    "kannada": "kn",
    "malayalam": "ml",
    "bengali": "bn",
    "urdu": "ur",
    "arabic": "ar",
    "french": "fr",
    "spanish": "es",
    "german": "de",
}

_last_spoken = ""
_last_time = 0
_lock = threading.Lock()


def speak_alert(text: str, language_name: str = "english", mode: str = "offline", cooldown: int = 4) -> str:
    global _last_spoken, _last_time

    now = time.time()

    with _lock:
        if text == _last_spoken and now - _last_time < cooldown:
            return text

        _last_spoken = text
        _last_time = now

    def runner():
        try:
            subprocess.Popen(["say", text])
        except Exception as exc:
            print("Voice error:", exc)

    threading.Thread(target=runner, daemon=True).start()
    return text
