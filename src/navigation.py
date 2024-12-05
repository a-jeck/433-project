import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import SCROLL_PAUSE_RANGE, PAUSE_FREQUENCY, SCROLL_AMOUNT, INERTIA_FACTOR, SCROLL_STEP_TIME, MAX_LOADING_WAIT

def scroll(driver, pause_range=SCROLL_PAUSE_RANGE, pause_frequency=PAUSE_FREQUENCY, scroll_amount=SCROLL_AMOUNT, inertia_factor = INERTIA_FACTOR):
    action = ActionChains(driver)
    current_position = 0
    end_of_page = False
    velocity = 0
    max_velocity = random.uniform(*scroll_amount)

    # wait for a tweet to load (else scrolling will stop)
    wait = WebDriverWait(driver, MAX_LOADING_WAIT)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))

    while not end_of_page:
        # simulate inertia-based scrolling
        if velocity < max_velocity:
            velocity += random.uniform(0, inertia_factor)

        # add random pauses to mimic a real person scrolling
        if random.uniform(0, 1) < pause_frequency:
            print("Pausing")
            time.sleep(random.uniform(*pause_range))
            find_tweet(driver)
            velocity = random.uniform(0, max_velocity * inertia_factor)
        
        # scroll
        current_position += velocity
        driver.execute_script(f"window.scrollTo(0, {current_position});")

        #decelerate slighly, with a little noise, without getting too extreme
        velocity *= (1 - inertia_factor/2)
        velocity += random.uniform(-inertia_factor/4, inertia_factor/4)
        velocity = max(min(velocity, max_velocity), -max_velocity)

        # add some mouse movement noise to mimic a real person scrolling
        # if random.uniform(0, 1) < 0.3:  # 30% chance to move the mouse
        #     action.move_by_offset(random.uniform(-3, 3), random.uniform(-3, 3)).perform()

        # check if end of page
        end_of_page = driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight")
        time.sleep(random.uniform(*SCROLL_STEP_TIME))

    print('scrolling ended')

def find_tweet(driver):
    print("read called")
    tweets = driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

    if tweets:

        # Some tweets are loaded before they are visible. We want visible tweets only. 
        visible_tweets = []
        for tweet in tweets:
           # use a script to check if the tweet is inside the viewport
           # rect.top >=0 ensures the tweet doesn't start above viewport
           # rect.bottom <=... ensures tweet doesn't end below the viewport (ends more than window height away from the top of the viewport)
           is_visible = driver.execute_script(
               """
                const rect = arguments[0].getBoundingClientRect();
                return rect.top >= 0 && rect.bottom <= window.innerHeight;
                """,
                tweet
           )
           if is_visible:
               visible_tweets.append(tweet)
        # select last visible tweet and read in the text. 
        if visible_tweets:
            last_tweet = visible_tweets[-1]
            tweet_text = last_tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').text
            tweet_id = last_tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]').get_attribute("id")
            return (tweet_text, tweet_id)
        else:
            print("No visible tweets")
    else: 
        print("no  tweets")


def get_response(tweet):
    NotImplemented