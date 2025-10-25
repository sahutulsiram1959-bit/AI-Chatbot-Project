from dotenv import load_dotenv
import os

env_path = "key.env"
load_dotenv(dotenv_path=env_path)
key = os.getenv("GENAI_API_KEY")

if key:
    print("✅ Key loaded successfully")
else:
    print("❌ Key not found")
