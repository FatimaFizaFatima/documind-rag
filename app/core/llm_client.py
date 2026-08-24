from google import genai

from app.core.config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(
    api_key=GEMINI_API_KEY
)


def generate_answer(prompt: str) -> str:

    response = client.models.generate_content(
        # model="gemini-3.7-flash",
        model = GEMINI_MODEL,
        contents=prompt
    )

    return response.text