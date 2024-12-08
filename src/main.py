import time
from bot import TwitterBot
from constants import VIDEO


bot = TwitterBot()

while(True):
    if bot.scroll() == 0:  
        if (bot.tweet.type == VIDEO):
            bot.download()
            bot.readTweet()

    time.sleep(10)
    # bot.readTweet()