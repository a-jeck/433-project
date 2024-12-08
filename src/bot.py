from navigation import scroll
from responses import get_response
from selenium import webdriver
from constants import URL
from config import AUTH_COOKIE

class TwitterBot:
    def __init__(self):
        # Launch Chrome, go to URL, login
        driver = webdriver.Chrome()
        driver.get(URL)
        driver.add_cookie(AUTH_COOKIE)
        driver.refresh()

        self.driver = driver
        self.current_position = 0
        self.end_of_page = False
        self.last_tweet = ("", "")

    def scroll(self):
        return(scroll(self))
    
    def readTweet(self):
        get_response(self.tweet)
        return