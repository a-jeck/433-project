import google.generativeai as genai
import PIL.Image
from config import GEMINI_API_KEY 
from constants import GEMINI_PROMPT, GEMINI_MODEL

def get_response(tweet):
    print("HERE GETTING RESPONSE!")
    genai.configure(api_key=GEMINI_API_KEY)
    img = PIL.Image.open('../assets/image.jpg')
    model = genai.GenerativeModel(GEMINI_MODEL)
    response = model.generate_content(["Tell me about this img", img])
    # response = model.generate_content(GEMINI_PROMPT + tweet[0])
    print(response.text)