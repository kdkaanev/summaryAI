from django.shortcuts import render

# Create your views here.
import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

import re
import requests
from bs4 import BeautifulSoup
from youtube_transcript_api import YouTubeTranscriptApi


def extract_content(url: str) -> str:
    """
    Връща текст от статия или YouTube видео.
    Ако няма транскрипция за YouTube, връща заглавие + описание.
    """

    # ---- YouTube обработка ----
    if "youtube.com" in url or "youtu.be" in url:
        video_id = None
        if "youtu.be" in url:
            video_id = url.split("/")[-1]
        else:
            match = re.search(r"v=([^&]+)", url)
            if match:
                video_id = match.group(1)
        if not video_id:
            return ""

        try:
            api = YouTubeTranscriptApi()
            transcript_data = api.fetch(video_id, languages=['bg', 'en'])

            texts = []
            for entry in transcript_data:
                if isinstance(entry, dict):
                    texts.append(entry.get("text", ""))
                else:
                    texts.append(getattr(entry, "text", ""))

            return " ".join(texts).strip()

        except (NoTranscriptFound, TranscriptsDisabled):
            try:
                # YouTube Data API / oEmbed за заглавие и описание
                oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
                meta = requests.get(oembed_url, timeout=5).json()

                # fallback описание
                description = get_video_description(video_id)
                return f"{meta.get('title', '')}\n\n{description}".strip()
            except Exception:
                return "Няма налична транскрипция или описание."
        except Exception as e:
            return f"Грешка при извличане на YouTube транскрипция: {e}"

    # ---- Уеб страница ----
    else:
        html = requests.get(url, timeout=10).text
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = [p.get_text() for p in soup.find_all("p")]
        return "\n".join(paragraphs)


def get_video_description(video_id: str) -> str:
    """
    Извлича описание на видео чрез yt-dlp (ако е наличен) или връща празно.
    """
    try:
        import yt_dlp
        ydl_opts = {"quiet": True, "skip_download": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            return info.get("description", "")
    except Exception:
        return ""

def summarize_text(text: str) -> dict:
    """Вика OpenAI API за обобщаване."""
    prompt = f"Обобщи следния текст на български с кратки ключови точки:\n\n{text}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    content = response.choices[0].message.content.strip()

    # Разделяне на обобщение и точки (ако са във формат)
    summary, points = content, []
    if "\n" in content:
        parts = content.split("\n")
        summary = parts[0]
        points = [p.strip("-• ") for p in parts[1:] if p.strip()]
    return {"summary": summary, "key_points": points}

@api_view(['POST'])
def summarize_view(request):
    url = request.data.get("url")
    if not url:
        return Response({"error": "URL е задължителен."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        text = extract_content(url)
        if not text.strip():
            return Response({"error": "Не можа да се извлече съдържание."}, status=status.HTTP_400_BAD_REQUEST)
        result = summarize_text(text)
        return Response(result)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
