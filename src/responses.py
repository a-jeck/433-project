import google.generativeai as genai
import PIL.Image
from config import GEMINI_API_KEY 
from constants import GEMINI_TEXT_PROMPT, GEMINI_IMAGE_PROMPT, GEMINI_TEXT_AND_IMAGE_PROMPT, GEMINI_MODEL

def get_response(tweet, image):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(GEMINI_MODEL)
    if (image and tweet.text):
        img = PIL.Image.open('../assets/image.jpg')
        response = model.generate_content([GEMINI_TEXT_AND_IMAGE_PROMPT, tweet.text, img])
    elif image:
        img = PIL.Image.open('../assets/image.jpg')
        response = model.generate_content([GEMINI_IMAGE_PROMPT, img])
    else:
        response = model.generate_content(GEMINI_TEXT_PROMPT + tweet[0])

    return(response.text)