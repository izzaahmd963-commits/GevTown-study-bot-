# check_models.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Configure API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models
print("📋 Available Gemini Models:\n")
for model in genai.list_models():
    if "gemini" in model.name:
        print(f"✅ {model.name}")
        print(f"   Display: {model.display_name}")
        print(f"   Methods: {model.supported_generation_methods}")
        print()