import os
from dotenv import load_dotenv

load_dotenv()

UPLOAD_DIR="data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")