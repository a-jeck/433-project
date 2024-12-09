import time
import random
import re
import requests
from io import BytesIO
from PIL import Image
from humancursor import WebCursor
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import SCROLL_STEP, MAX_LOADING_WAIT, ACCELERATION, IMAGE, VIDEO, TEXT, TIMESTAMP_REGEX
from responses import get_response
from tweet import Tweet

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
   
    # Move the next tweet to the middle of the page # execute the distance above
    distance_scrolled = 0
    velocity = 0
    last_acceleration = ACCELERATION
    while distance_scrolled < scroll_distance:

        # Slowly speed up each 'scroll'
        last_acceleration = random.uniform(last_acceleration, last_acceleration + last_acceleration // 2)
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
        time.sleep(SCROLL_STEP)

    # Extract type from the tweet
    tweet_body = middle_tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="tweetText"]')
    tweet_image = middle_tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="tweetPhoto"]')
    tweet_video = middle_tweet_element.find_elements(By.CSS_SELECTOR, '[data-testid="videoPlayer"]')

    tweet_type = VIDEO if tweet_video else IMAGE if tweet_image else TEXT
   
    # Create tweet and add attributes
    processed_tweet = Tweet(tweet_type)
    if tweet_body and tweet_body[0].text: # Quote tweets can have two tweetTexts
        processed_tweet.text = tweet_body[0].text

    if tweet_type == VIDEO:
        video_div = tweet_video[0].get_attribute("outerHTML")
        video_time = re.search(TIMESTAMP_REGEX, video_div)
        if video_time: 
            video_length = video_time.group(0).split(':')
            processed_tweet.minutes = video_length[0]
            processed_tweet.seconds = video_length[1]
    
    # Videos have an image preview
    if tweet_type == IMAGE:
        media_div = tweet_image[0].get_attribute("outerHTML")
        image_search = re.search(r'https://pbs\.twimg\.com/[^\s"]+jpg', media_div)
        if image_search:
            processed_tweet.link = image_search.group(0)
    if tweet_type == VIDEO:
        media_div = tweet_video[0].get_attribute("outerHTML")
        image_search = re.search(r'https://pbs\.twimg\.com/[^\s"]+jpg', media_div)
        if image_search:
            processed_tweet.link = image_search.group(0)
    bot.tweet = processed_tweet
    return(0)


def downloadImage(tweet):
    if tweet.link:
        try:
            response = requests.get(tweet.link)
            response.raise_for_status() 

            image = Image.open(BytesIO(response.content))

            # Save the image to the specified path
            image.save('../assets/image.jpg')
            print(f"Image successfully downloaded")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download image: {e}")
        except IOError as e:
            print(f"Failed to save image: {e}")

def findLikeButton(bot):
    # Find middle of page
    viewport_height = bot.driver.execute_script("return window.innerHeight;")
    viewport_middle_axis = viewport_height // 2

    # Find first like button below middle of page
    like_buttons = bot.driver.find_elements(By.CSS_SELECTOR, '[data-testid="like"]')
    for button in like_buttons:
        heart_icon = button.find_element(By.CSS_SELECTOR, "svg")
        top = bot.driver.execute_script(
            """
            return(arguments[0].getBoundingClientRect().top);
            """, heart_icon
        )
        if (top > viewport_middle_axis):
            return heart_icon
    return -1


def click(bot, target):
    x_offset = random.uniform(0.1, 0.9)
    y_offset = random.uniform(0.1, 0.9)
    click_duration = random.uniform(0.04, 0.08)
    bot.cursor.click_on(target, relative_position=[x_offset, y_offset], click_duration = click_duration)
    return

def randomMouseMovement(bot):
    x_offset = random.uniform(10, 100)
    y_offset = random.uniform(10, 100)
    bot.cursor.show_cursor()
    bot.cursor.move_to([x_offset, y_offset], absolute_offset=True)
    return



