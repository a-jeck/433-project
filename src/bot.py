import random, time
from selenium import webdriver
from humancursor import WebCursor

from navigation import scrollToNextTweet, downloadImage, findButton
from mouse_actions import  click, randomMouseMovement, randomClick
from keyboard_actions import typeStr, submitField
from responses import get_response

from constants import URL, LIKE, RETWEET, REPLY, REPLY_TOGGLE_TYPING_PAUSE_RANGE, RETWEET_DOUBLECLICK_COOLDOWN_RANGE
from config import AUTH_COOKIE

class TwitterBot:
    def __init__(self):
        # Launch Chrome, go to URL, login
        driver = webdriver.Chrome()
        driver.get(URL)
        driver.add_cookie(AUTH_COOKIE)
        driver.refresh()
        cursor = WebCursor(driver)

        self.driver = driver
        self.cursor = cursor
        self.current_position = 0
        self.end_of_page = False
        self.last_tweet = ("", "")
        self.tweet = None

    def scroll(self):
        return(scrollToNextTweet(self))
    
    def readTweet(self, image):
        return get_response(self.tweet, image)
        
    def download(self):
        downloadImage(self.tweet)
        return
    
    def like(self):
        target = findButton(self, LIKE)
        click(self, target)
        randomMouseMovement(self)
        return
    
    def retweet(self):
        target = findButton(self, RETWEET)
        click(self, target)
        time.sleep(random.uniform(*RETWEET_DOUBLECLICK_COOLDOWN_RANGE))
        randomClick(self)
        randomMouseMovement(self)
        return
    
    def reply(self, text):
        target = findButton(self, REPLY)
        click(self, target)
        time.sleep(random.uniform(*REPLY_TOGGLE_TYPING_PAUSE_RANGE))
        typeStr(self, text)
        time.sleep(random.uniform(*REPLY_TOGGLE_TYPING_PAUSE_RANGE))
        submitField(self)
        randomMouseMovement(self)
        return
    