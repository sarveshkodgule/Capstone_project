import os
import json
import urllib.request
from dotenv import load_dotenv
from database.mongodb import chat_history_collection
from schemas.chatbot import ChatQuery
from datetime import datetime

# Load .env explicitly using absolute path to prevent startup directory issues
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
env_path = os.path.join(base_dir, ".env")
load_dotenv(dotenv_path=env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"


def _call_gemini(prompt: str) -> str:
    """Call Gemini REST API directly using only stdlib urllib - no external packages needed."""
    if not GEMINI_API_KEY:
        return None  # Signal that we should use fallback

    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    data = json.dumps(payload).encode("utf-8")
    url = f"{GEMINI_URL}?key={GEMINI_API_KEY}"

    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            return body["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return None


def get_chatbot_response(message: str) -> str:
    prompt = (
        "You are a helpful Myopia Screening Assistant for a medical application. "
        f"A logged-in patient asks: {message}. "
        "Give a concise, professional, and medically sound response about myopia, eye health, or related topics."
    )
    result = _call_gemini(prompt)
    if result:
        return result

    # Offline fallback
    msg = message.lower()
    if "myopia" in msg:
        return "Myopia (nearsightedness) is a condition where close objects are clear but distant ones are blurry. Regular check-ups are recommended."
    elif "screen" in msg:
        return "Excessive screen time is a known risk factor. Try the 20-20-20 rule: every 20 min, look 20 feet away for 20 seconds."
    elif "hi" in msg or "hello" in msg:
        return "Hello! I'm your Vision AI Assistant. Ask me anything about myopia or eye health."
    else:
        return "I'm here to help with questions about myopia and eye health. Please consult your ophthalmologist for personalized advice."


async def process_chat_query(user_id: str, query: ChatQuery):
    response_text = get_chatbot_response(query.message)
    chat_record = {
        "user_id": user_id,
        "message": query.message,
        "response": response_text,
        "timestamp": datetime.now().isoformat()
    }
    await chat_history_collection.insert_one(chat_record)
    return {"response": response_text}


def get_general_chatbot_response(message: str) -> str:
    prompt = (
        "You are a welcoming Myopia Screening Clinic AI assistant on the home page. "
        f"A prospective visitor asks: {message}. "
        "Provide a friendly, concise response about myopia, the clinic's services, or guide them to create an account."
    )
    result = _call_gemini(prompt)
    if result:
        return result
    return "Welcome! I'm the VisionAssistant AI. I can answer questions about myopia and how our clinic can help. Please sign up to access full features!"
