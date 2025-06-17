from app.core.config import Config
from groq import Groq


def get_groq_client():
    return Groq(api_key=Config.GROQ_API_KEY)
