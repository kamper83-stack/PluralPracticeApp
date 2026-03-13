#!/usr/bin/env python3
"""
YouTube Video Summarizer
מסכם סרטוני יוטיוב בעברית לניהול פרויקטים מבוסס AI
"""

import sys
import re
import argparse
from urllib.parse import urlparse, parse_qs

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
except ImportError:
    print("שגיאה: חסרה חבילת youtube-transcript-api")
    print("הרץ: pip install youtube-transcript-api")
    sys.exit(1)

try:
    import anthropic
except ImportError:
    print("שגיאה: חסרה חבילת anthropic")
    print("הרץ: pip install anthropic")
    sys.exit(1)


def extract_video_id(url: str) -> str:
    """חולץ את מזהה הסרטון מ-URL של יוטיוב."""
    patterns = [
        r'(?:v=|youtu\.be/|embed/|v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$',
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError(f"לא ניתן לחלץ מזהה סרטון מ: {url}")


def get_transcript(video_id: str) -> str:
    """מחלץ תמליל מסרטון יוטיוב."""
    try:
        # נסה קודם בעברית, אחר כך באנגלית, אחר כך כל שפה זמינה
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        transcript = None
        try:
            transcript = transcript_list.find_transcript(['he', 'iw'])
        except NoTranscriptFound:
            pass

        if transcript is None:
            try:
                transcript = transcript_list.find_transcript(['en'])
            except NoTranscriptFound:
                pass

        if transcript is None:
            # קח כל תמליל זמין
            transcript = transcript_list.find_transcript(
                [t.language_code for t in transcript_list]
            )

        entries = transcript.fetch()
        full_text = " ".join(entry.text for entry in entries)
        return full_text

    except TranscriptsDisabled:
        raise RuntimeError("תמלילים מושבתים עבור סרטון זה")
    except NoTranscriptFound:
        raise RuntimeError("לא נמצא תמליל עבור סרטון זה")
    except Exception as e:
        raise RuntimeError(f"שגיאה בחילוץ תמליל: {e}")


def summarize_with_claude(video_url: str, transcript: str) -> str:
    """מסכם את התמליל באמצעות Claude API."""
    client = anthropic.Anthropic()

    prompt = f"""אתה מומחה לסיכום תוכן וידאו עבור מנהל פרויקטים שעובד עם AI.

להלן תמליל של סרטון יוטיוב מ: {video_url}

תמליל הסרטון:
---
{transcript[:15000]}
---

אנא סכם את הסרטון בדיוק בפורמט הבא (בעברית):

## 1. תיאור כללי
[תיאור קצר ותמציתי של הסרטון - 2-3 משפטים]

## 2. מהות היכולת / הרעיון המרכזי
[מה הכלי/השיטה/הרעיון שהסרטון מציג? מה הוא עושה ואיך?]

## 3. Use Cases - ניהול פרויקטים מבוסס AI
[3-5 use cases ספציפיים ומעשיים עבור מנהל פרויקטים שמשתמש ב-AI בעבודתו היומיומית. לדוגמה: אוטומציה של משימות, ניתוח נתוני פרויקט, שיפור תקשורת עם הצוות, כתיבת מסמכים, מעקב אחר התקדמות וכו']

## 4. התקנה
[הוראות התקנה שלב אחר שלב - אם מוזכרות בסרטון. אם לא מוזכרות, כתוב "לא הוזכר בסרטון"]

## 5. שימוש
[איך משתמשים בכלי/שיטה? דוגמאות קונקרטיות - אם מוזכרות בסרטון]

חשוב: כתוב הכל בעברית, היה ספציפי ומעשי."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}]
    )

    return message.content[0].text


def main():
    parser = argparse.ArgumentParser(
        description="מסכם סרטוני יוטיוב בעברית לניהול פרויקטים מבוסס AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
דוגמאות שימוש:
  python summarize.py https://www.youtube.com/watch?v=VIDEO_ID
  python summarize.py https://youtu.be/VIDEO_ID
  python summarize.py VIDEO_ID
        """
    )
    parser.add_argument(
        "url",
        help="קישור לסרטון יוטיוב או מזהה סרטון"
    )
    parser.add_argument(
        "--output", "-o",
        help="שמור סיכום לקובץ (אופציונלי)",
        default=None
    )
    parser.add_argument(
        "--transcript-only", "-t",
        action="store_true",
        help="הצג רק את התמליל ללא סיכום"
    )

    args = parser.parse_args()

    print(f"מעבד סרטון: {args.url}")
    print("חולץ תמליל...")

    try:
        video_id = extract_video_id(args.url)
    except ValueError as e:
        print(f"שגיאה: {e}")
        sys.exit(1)

    try:
        transcript = get_transcript(video_id)
    except RuntimeError as e:
        print(f"שגיאה: {e}")
        sys.exit(1)

    if args.transcript_only:
        print("\n--- תמליל ---")
        print(transcript)
        return

    print(f"תמליל חולץ ({len(transcript)} תווים). מסכם עם Claude...")

    try:
        summary = summarize_with_claude(args.url, transcript)
    except Exception as e:
        print(f"שגיאה בסיכום: {e}")
        sys.exit(1)

    print("\n" + "="*60)
    print(summary)
    print("="*60)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(f"סיכום סרטון: {args.url}\n\n")
            f.write(summary)
        print(f"\nסיכום נשמר ל: {args.output}")


if __name__ == "__main__":
    main()
