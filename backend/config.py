import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    ALGORITHM = os.getenv("ALGORITHM", "")
    GROQ_MODEL = os.getenv("GROQ_MODEL", "")
