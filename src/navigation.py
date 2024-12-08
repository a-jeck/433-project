import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import SCROLL_PAUSE_RANGE, SCROLL_STEP_TIME, MAX_LOADING_WAIT
from responses import get_response

def scroll(bot):
    # Wait for page load
    wait = WebDriverWait(bot.driver, MAX_LOADING_WAIT)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))

    # Find the middle of the page
    viewport_height = bot.driver.execute_script("return window.innerHeight;")
    viewport_middle_axis = viewport_height // 2

    # Find the tweet below the middle of the page (whichever the first tweet who's top of the their box is below middle)
    tweets = bot.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

    middle_tweet_element = None
    middle_tweet_bounds = None
    for tweet in tweets:
        tweet_bounds = bot.driver.execute_script(
            """
            var rect = arguments[0].getBoundingClientRect();
            return {top: rect.top, bottom: rect.bottom};
            """, tweet
        )
        if tweet_bounds['top'] > viewport_middle_axis:
            middle_tweet_element = tweet
            middle_tweet_bounds = tweet_bounds
            break
    
    if not middle_tweet_element or middle_tweet_element == bot.last_tweet:
        return
    else:
        bot.last_tweet = middle_tweet_element
    
    # Calculate the distance needed to place the 'next tweet' in the middle of the page, with at least 25% of it above and below the middle line
    middle_tweet_height = middle_tweet_bounds['bottom'] - middle_tweet_bounds['top']
    scroll_distance_variance = middle_tweet_height // 4
    min_scroll_distance = middle_tweet_bounds['top'] - viewport_middle_axis + scroll_distance_variance
    max_scroll_distance = middle_tweet_bounds['bottom'] - viewport_middle_axis - scroll_distance_variance
    scroll_distance = random.uniform(min_scroll_distance, max_scroll_distance)
    
    print("Tweet height:", middle_tweet_height)
    print("Tweet top:", middle_tweet_bounds['top'])
    print("Tweet botom:", middle_tweet_bounds['bottom'])
    print("min scroll", min_scroll_distance)
    print("max scroll", max_scroll_distance)
    

    print(scroll_distance)

    # Move the next tweet to the middle of the page # execute the distance above
    distance_scrolled = 0
    velocity = 0
    last_acceleration = 0.25
    while distance_scrolled < scroll_distance:

        # Slowly speed up each 'scroll'
        last_acceleration = random.uniform(last_acceleration, last_acceleration + last_acceleration//2)
        velocity += last_acceleration

        # Do not scroll past target
        distance_remaining = scroll_distance - distance_scrolled
        if (distance_remaining < velocity): 
            velocity = distance_remaining
        distance_scrolled += velocity

        # Scroll
        bot.current_position += velocity
        bot.driver.execute_script(f"window.scrollTo(0, {bot.current_position});")

        # Pause
        time.sleep(0.025)

    tweetBody = middle_tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
    
    # posts with only images or videos have no tweetText
    if not tweetBody:
        return
    # Quote tweets have two tweetTexts
    target_tweet = tweetBody[0]

    tweet_text = target_tweet.text
    tweet_id = target_tweet.get_attribute("id")
    # bot.tweet = tweet
    print(tweet_text, tweet_id)
    return

# def scroll(bot):
#     # wait for a tweets to load
#     wait = WebDriverWait(bot.driver, MAX_LOADING_WAIT)
#     wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweet"]')))
#     max_velocity = 12
#     velocity = 0
#     acceleration = 0.5  # Control the rate of acceleration
#     deceleration = 0.5  # Control the rate of deceleration
#     SCROLL_STEP_TIME = 0.05  # Interval for each scroll step (in seconds)
#     SCROLL_PAUSE_RANGE = (0.5, 1.5)  # Range for pause after finding a tweet

#     while not bot.end_of_page:
#         if velocity < max_velocity:
#             velocity += random.uniform(acceleration / 2, acceleration)
#         else:
#             # Gradually decelerate as we approach the end of the page
#             if bot.end_of_page:
#                 velocity *= 0.9  # Decelerate to simulate a smooth stop

#         # Update the current position
#         bot.current_position += velocity
#         bot.driver.execute_script(f"window.scrollTo(0, {bot.current_position});")

#         # Check if a tweet is found and is not the last one
#         tweet = find_tweet(bot)
#         if tweet and tweet[1] != bot.last_tweet[1]:
#             time.sleep(random.uniform(*SCROLL_PAUSE_RANGE))
#             bot.last_tweet = tweet
#             bot.tweet = tweet
#             return 0

#     # Check if we have reached the bottom of the page
#     bot.end_of_page = bot.driver.execute_script("return (window.innerHeight + window.scrollY) >= document.body.scrollHeight")
#     print(f"Velocity: {velocity:.2f}")
#     time.sleep(SCROLL_STEP_TIME)

#     print('scrolling ended')

# def find_tweet(bot):
#     tweets = bot.driver.find_elements(By.CSS_SELECTOR, '[data-testid="tweet"]')

#     if tweets:
#         # Some tweets are loaded before they are visible. We want visible tweets only. 
#         visible_tweets = []
#         for tweet in tweets:
#            # use a script to check if the tweet is inside the viewport
#            # rect.top >=0 ensures the tweet doesn't start above viewport
#            # rect.bottom <=... ensures tweet doesn't end below the viewport (ends more than window height away from the top of the viewport)
#            is_visible = bot.driver.execute_script(
#                """
#                 const rect = arguments[0].getBoundingClientRect();
#                 return rect.top >= 0 && rect.bottom <= window.innerHeight;
#                 """,
#                 tweet
#            )
#            if is_visible:
#                visible_tweets.append(tweet)
#         # select last visible tweet and read in the text. 
#         if visible_tweets:
#             bottom_tweet = visible_tweets[-1]
#             tweetBody = WebDriverWait(bottom_tweet, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="tweetText"]')))
#             tweet_text = tweetBody.text
#             tweet_id = tweetBody.get_attribute("id")
#             print("Adding tweet")
#             print(tweet_text)
#             print(tweet_id)
#             return (tweet_text, tweet_id)
#         else:
#             return
#     else: 
#         return


