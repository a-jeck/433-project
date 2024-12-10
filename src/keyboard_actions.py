import random, time, re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def calculate_typing_time(base_wpm=70, variation=10):
    current_wpm = base_wpm + random.uniform(-variation, variation)
    chars_per_minute = current_wpm * 5 
    return 1 / (chars_per_minute / 60)

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
    
    if random.random() < 0.2:
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
    cleaned_text = re.sub(r'[^\w\s.,!?\'\";:-]', '', text)
    # Remove leftover spaces from first cleaning
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()

    for char in cleaned_text:
        # Generate potential typo
        typo_char, is_typo = generate_typo(char)
        
        # If typo occurred, type the wrong character first then correct
        if is_typo:
            input_field.send_keys(typo_char)
            time.sleep(random.uniform(0.2, 0.5))
            input_field.send_keys('\b')
            time.sleep(random.uniform(0.1, 0.2))
        
        # Type the correct character
        input_field.send_keys(char)
        
        # Calculate and apply typing time
        type_time = calculate_typing_time()
        time.sleep(type_time)
        
        # Random pauses between characters
        if random.random() < 0.1:
            time.sleep(random.uniform(0.1, 0.3))


def submitField(bot):
    input_field = bot.driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"][contenteditable="true"]')
    actions = ActionChains(input_field.parent)

    # Send CTRL + Enter
    actions.key_down(Keys.CONTROL)
    actions.send_keys(Keys.ENTER)
    actions.key_up(Keys.CONTROL)
    actions.perform()

    time.sleep(0.5)