# import whisper

# model = whisper.load_model("tiny")

# def transcribe_audio(file_path):
#     result = model.transcribe(file_path)
#     return result["text"]


import os
from typing import Optional
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

HALLUCINATION_PHRASES = [
    "thank you for watching",
    "thanks for watching",
    "please subscribe",
    "transcribe every line",
    "song lyrics with music",
]

NO_SPEECH_THRESHOLD = 0.6

# Debug ke liye True rakho. Sab theek hone ke baad True se False kar dena.
DEBUG_DISABLE_FILTER = True


def _get(obj, key, default=None):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def transcribe_audio(
    file_path: str,
    language: Optional[str] = None,
    is_lyrics: bool = True,  # main.py compatibility ke liye rakha hai
) -> str:
    params = {
        "model": "whisper-large-v3",
        "temperature": 0,
        "response_format": "verbose_json",
    }

    if language:
        params["language"] = language  # e.g. "hi", "en", "pa"

    with open(file_path, "rb") as f:
        result = client.audio.transcriptions.create(
            file=f,
            **params
        )

    segments = _get(result, "segments", None) or []

    print("RAW TEXT:", _get(result, "text", ""))
    for seg in segments:
        print(
            round(_get(seg, "no_speech_prob", 0) or 0, 2),
            "|",
            (_get(seg, "text", "") or "").strip()
        )

    if not segments:
        return (_get(result, "text", "") or "").strip()

    lines = []
    for seg in segments:
        text = (_get(seg, "text", "") or "").strip()
        no_speech = _get(seg, "no_speech_prob", 0) or 0

        if not text:
            continue

        if not DEBUG_DISABLE_FILTER:
            if no_speech > NO_SPEECH_THRESHOLD:
                continue
            if any(p in text.lower() for p in HALLUCINATION_PHRASES):
                continue

        lines.append(text)

    return "\n".join(lines)