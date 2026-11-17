import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

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