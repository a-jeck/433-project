import random
import time
from navigation import scroll, downloadImage, naturalText, randomClick, findButton, click, randomMouseMovement
from responses import get_response
from selenium import webdriver
from humancursor import WebCursor
from constants import URL, LIKE, RETWEET, REPLY
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
        return(scroll(self))
    
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
        time.sleep(random.uniform(0.2, 0.6))
        randomClick(self)
        randomMouseMovement(self)
        return
    
    def reply(self):
        target = findButton(self, REPLY)
        click(self, target)
        naturalText(self, "blah")
        time.sleep(5)
        randomMouseMovement(self)
        return
    