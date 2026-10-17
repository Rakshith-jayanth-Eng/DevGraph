import os

from dotenv import load_dotenv
from google import genai

load_dotenv(override=True)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=(
            "You are helping a developer debug an API. "
            "In one sentence, explain why a missing JWT "
            "Authorization header can cause an HTTP 401 error."
        ),
    )

    print("Gemini connection successful!")
    print(response.text)

except Exception as error:
    print(f"Gemini test failed: {type(error).__name__}")
    print(str(error))