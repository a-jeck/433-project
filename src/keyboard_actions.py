import random, time, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from constants import BASE_WPM, WPM_VARIATION, WPM_TO_CPM_RATIO, TYPO_PROBABILITY, REALIZE_TYPO_PAUSE_RANGE, FIX_TYPO_PAUSE_RANGE, SANITIZE_GEMINI_RESPONSE_REGEX, REMOVE_MULTI_SPACES_REGEX, TYPING_PAUSE_PROB, TYPING_PAUSE_RANGE

def calculate_typing_time():
    current_wpm = BASE_WPM + random.uniform(-WPM_VARIATION, WPM_VARIATION)
    chars_per_minute = current_wpm * WPM_TO_CPM_RATIO 
    seconds_per_min = 60
    return 1 / (chars_per_minute / seconds_per_min)

def generate_typo(char):
    if len(char) != 1:
        return (char, False)
    
    # Keyboard proximity typos
    typo_map = {
        'q': 'wa', 'w': 'qae', 'e': 'wdr', 'r': 'etf', 't': 'rgy', 
        'y': 'tuh', 'u': 'yih', 'i': 'uoj', 'o': 'ip', 'p': 'o[',
        'a': 'qsz', 's': 'awdz', 'd': 'sefc', 'f': 'drgv', 
        'g': 'fthb', 'h': 'gyjn', 'j': 'hukm', 'k': 'jil', 'l': 'ko;',
        'z': 'axs', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 
        'b': 'vghn', 'n': 'bhj', 'm': 'njk'
    }
    
    if random.random() < TYPO_PROBABILITY:
        if char.lower() in typo_map:
            # Select a random key near desired key
            typo_char = random.choice(typo_map[char.lower()])
            # Preserve original case
            return (typo_char.upper() if char.isupper() else typo_char, True)
    return (char, False)

def typeStr(bot, text):
    input_field = bot.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"][contenteditable="true"]')

    # Remove emojis and other unwanted characters
    # Keep alphanumeric, spaces, and common punctuation
    cleaned_text = re.sub(SANITIZE_GEMINI_RESPONSE_REGEX, '', text)
    # Remove leftover spaces from first cleaning
    cleaned_text = re.sub(REMOVE_MULTI_SPACES_REGEX, ' ', cleaned_text).strip()

    for char in cleaned_text:
        # Generate potential typo
        typo_char, is_typo = generate_typo(char)
        
        # If typo occurred, type the wrong character first then correct
        if is_typo:
            input_field.send_keys(typo_char)
            time.sleep(random.uniform(REALIZE_TYPO_PAUSE_RANGE))
            input_field.send_keys('\b')
            time.sleep(random.uniform(FIX_TYPO_PAUSE_RANGE))
        
        # Type the correct character
        input_field.send_keys(char)
        
        # Calculate and apply typing time
        type_time = calculate_typing_time()
        time.sleep(type_time)
        
        # Random pauses between characters
        if random.random() < TYPING_PAUSE_PROB:
            time.sleep(random.uniform(TYPING_PAUSE_RANGE))


def submitField(bot):
    input_field = bot.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"][contenteditable="true"]')
    actions = ActionChains(input_field.parent)

    # Send CTRL + Enter
    actions.key_down(Keys.CONTROL)
    actions.send_keys(Keys.ENTER)
    actions.key_up(Keys.CONTROL)
    actions.perform()