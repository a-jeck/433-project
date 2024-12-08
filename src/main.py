from bot import TwitterBot


bot = TwitterBot()

while(True):
    bot.scroll()
    bot.readTweet()