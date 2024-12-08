import google.generativeai as genai
from config import GEMINI_API_KEY 
from constants import GEMINI_PROMPT, GEMINI_MODEL

def get_response(tweet):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(GEMINI_PROMPT + tweet[0])
    print(response.text)