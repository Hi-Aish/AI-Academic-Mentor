import os
from dotenv import load_dotenv

# Load environment variables from the .env file in the parent directory
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from environment variables or .env file.")