# import os
# from anthropic import Anthropic
# from dotenv import load_dotenv

# load_dotenv()

# client = Anthropic(
#     api_key=os.getenv("ANTHROPIC_API_KEY")
# )

# def generate_summary(transcript: str):
#     if not transcript:
#         return ["No transcript available"]

#     prompt = f"""
# The following text is either a speech/conversation transcript or song lyrics.
# If it is song lyrics, summarize the theme, mood and story of the song.
# If it is speech, summarize the key points.
# Return only bullet points, one per line.

# Transcript:
# {transcript}
# """

#     response = client.messages.create(
#         model="claude-sonnet-4-5",
#         max_tokens=500,
#         temperature=0.2,
#         messages=[
#             {"role": "user", "content": prompt}
#         ]
#     )

#     text = response.content[0].text

#     lines = [
#         line.lstrip("-•* ").strip()
#         for line in text.split("\n")
#         if line.strip()
#     ]

#     return lines




import os
import re
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

# Urdu / Arabic script ka Unicode range
URDU_PATTERN = re.compile(r"[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]")


def has_urdu_script(text: str) -> bool:
    return bool(URDU_PATTERN.search(text or ""))


def ensure_devanagari(text: str) -> str:
    """Agar text Urdu script me hai to use Devanagari (Hindi) me convert karta hai."""
    if not text or not has_urdu_script(text):
        return text

    prompt = f"""
Convert the following Urdu-script text into Hindi Devanagari script.
This is a transliteration only: do NOT translate, do NOT change the words,
do NOT add or remove anything. Keep the same line breaks.
Return only the converted text, nothing else.

Text:
{text}
"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=2000,
            temperature=0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        converted = response.content[0].text.strip()
        return converted or text
    except Exception as e:
        print("Devanagari conversion failed:", e)
        return text  # fail ho jaye to original transcript hi return karo


def generate_summary(transcript: str):
    if not transcript:
        return ["No transcript available"]

    prompt = f"""
The following text is either a speech/conversation transcript or song lyrics.
If it is song lyrics, summarize the theme, mood and story of the song.
If it is speech, summarize the key points.
Return only bullet points, one per line.

Transcript:
{transcript}
"""

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        temperature=0.2,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    text = response.content[0].text

    lines = [
        line.lstrip("-•* ").strip()
        for line in text.split("\n")
        if line.strip()
    ]

    return lines