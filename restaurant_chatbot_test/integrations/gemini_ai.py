import google.generativeai as genai
from data.given_data import INSTUCTIONS
from config import GEMINI_API_KEY

#  Configure API Key
genai.configure(api_key=GEMINI_API_KEY)

def get_gemini_response(user_input):
    """Fetches AI-generated responses from Gemini AI."""
    try:
       
        model = genai.GenerativeModel("gemini-1.5-pro")

        #  Generate response from Gemini AI
        response = model.generate_content(f"{INSTUCTIONS}\nUser: {user_input}")

        #  Extract and return text response
        return response.text if response and hasattr(response, "text") else "I'm sorry, I couldn't process your request."
              #hasattr() is a built-in Python function used to check whether rresponse has attribute text
    except Exception as e:
        print("Google Gemini API error:", e)
        return "Sorry, I couldn't process your request. Please try again later."
