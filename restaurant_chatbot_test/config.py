import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER", "whatsapp:+14155238886")

#supabase
key=os.getenv("SUPA_KEY")
url=os.getenv("SUPA_URL")
# Google Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")