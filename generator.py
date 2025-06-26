import os
import requests
from dotenv import load_dotenv
import json
import re

load_dotenv()

def generate_questions(app_name, goal, mandatory):
    API_KEY = os.getenv("GEMINI_API_KEY")
    if not API_KEY:
        raise Exception("GEMINI_API_KEY not found in .env file")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}

    prompt = f"""
    You're a UX researcher. Generate 10 user survey questions for an app called '{app_name}'.
    Survey goal: {goal}
    Mandatory questions to include: {mandatory}

    For each question, return:
    1. The full question text
    2. The appropriate field type — one of: Short Answer, Paragraph, Multiple Choice, Checkboxes, Range (0–10)
    3. If field type is Multiple Choice or Checkboxes, include 3–5 relevant options.
    4. If field type is Range, assume 0–10 scale with appropriate label.

    Output the response in JSON format like:
    [
      {{
        "question": "How often do you exercise?",
        "field_type": "Multiple Choice",
        "options": ["Daily", "Weekly", "Rarely", "Never"]
      }},
      {{
        "question": "On a scale of 0–10, how satisfied are you with your current fitness level?",
        "field_type": "Range"
      }}
    ]
    """

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        res = requests.post(url, headers=headers, json=payload)
        res.raise_for_status()
        content = res.json()['candidates'][0]['content']['parts'][0]['text']

        # Extract content between ```json and ```
        match = re.search(r"```json\n(.*?)```", content, re.DOTALL)
        if match:
            content_clean = match.group(1).strip()
        else:
            # Fallback: remove any backticks and attempt to parse
            content_clean = re.sub(r"```.*?\n|```", "", content).strip()

        questions = json.loads(content_clean)
        return questions

    except Exception as e:
        print("Error from Gemini:", e)
        print("Full response:", res.text if 'res' in locals() else 'No response')
        return [{"question": "(Error generating questions)", "field_type": "Short Answer"}]