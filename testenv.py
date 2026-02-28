import os
from dotenv import load_dotenv

load_dotenv()
print(f"API Key loaded successfully: {os.getenv('GOOGLE_API_KEY') is not None}")