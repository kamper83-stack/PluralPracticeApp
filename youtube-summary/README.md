# YouTube Summary - מסכם סרטוני יוטיוב

כלי Python לסיכום אוטומטי של סרטוני יוטיוב בעברית, מותאם לניהול פרויקטים מבוסס AI.

## מה הכלי עושה?

1. מחלץ תמליל אוטומטית מהדף של יוטיוב
2. שולח לClaude API לסיכום חכם
3. מחזיר סיכום מובנה בעברית הכולל:
   - תיאור כללי של הסרטון
   - מהות היכולת/הרעיון המרכזי
   - Use cases לניהול פרויקטים מבוסס AI
   - הוראות התקנה
   - הוראות שימוש

## דרישות מקדימות

- Python 3.8+
- מפתח API של Anthropic (Claude)

## התקנה

```bash
# שכפל או הורד את הקבצים
cd youtube-summary

# התקן את התלויות
pip install -r requirements.txt

# הגדר את מפתח ה-API
export ANTHROPIC_API_KEY="your-api-key-here"
```

## שימוש

```bash
# סיכום בסיסי
python summarize.py https://www.youtube.com/watch?v=VIDEO_ID

# סיכום עם שמירה לקובץ
python summarize.py https://youtu.be/VIDEO_ID --output summary.md

# רק תמליל (ללא סיכום)
python summarize.py https://www.youtube.com/watch?v=VIDEO_ID --transcript-only

# עם מזהה סרטון ישיר
python summarize.py dQw4w9WgXcQ
```

## פורמט הפלט

הכלי מחזיר סיכום מובנה:

```
## 1. תיאור כללי
[תיאור קצר של הסרטון]

## 2. מהות היכולת
[מה הסרטון מציג ואיך זה עובד]

## 3. Use Cases - ניהול פרויקטים מבוסס AI
[use cases ספציפיים לעבודה שלך]

## 4. התקנה
[הוראות התקנה מהסרטון]

## 5. שימוש
[איך להשתמש בכלי/שיטה]
```

## הגדרת מפתח API

```bash
# Linux/Mac - הוסף ל-~/.bashrc או ~/.zshrc
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows
set ANTHROPIC_API_KEY=sk-ant-...
```

## פתרון בעיות

| שגיאה | פתרון |
|-------|-------|
| `TranscriptsDisabled` | לסרטון אין תמליל זמין |
| `NoTranscriptFound` | נסה סרטון אחר |
| `AuthenticationError` | בדוק את מפתח ה-ANTHROPIC_API_KEY |
