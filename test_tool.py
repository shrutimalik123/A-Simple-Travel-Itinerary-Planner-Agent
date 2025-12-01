import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def get_current_weather(city: str) -> str:
    """
    Returns the current weather for a given city.
    """
    city = city.lower()
    if "rome" in city:
        return "sunny"
    elif "san francisco" in city:
        return "foggy"
    else:
        return "clear"

api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

try:
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents="What is the weather in San Francisco?",
        config=types.GenerateContentConfig(
            tools=[get_current_weather]
        )
    )
    print("Success!")
    print(response.text)
except Exception as e:
    print(f"Error: {e}")
