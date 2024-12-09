import time
import random
from bot import TwitterBot
from constants import VIDEO, IMAGE, TEXT


bot = TwitterBot()

while(True):
    if bot.scroll() == 0:
        # Glance at tweet, decide whether to engage
        time.sleep(random.uniform(0,2))
     
        # Chance of "reading" the tweet
        if random.uniform(0, 1) < 0.5:

            # Read the tweet
            response = None
            if (bot.tweet.type == VIDEO or bot.tweet.type == IMAGE):
                bot.download()
                response = bot.readTweet(image=True)
            else: 
                response = bot.readTweet(image=False)
            
            if (bot.tweet.text):
                print(bot.tweet.text)
            print(response)
            
            # This is something we want to engage in
            if (response.strip() != "No."):
                print("engage!")

                # Pause to "read" or "look" at it
                if (bot.tweet.type == VIDEO):
                    seconds = int(bot.tweet.seconds) + int(bot.tweet.minutes) * 60
              
                    quarter_video = 0.25 * seconds
                    time.sleep(random.uniform(quarter_video, seconds))
                elif (bot.tweet.type == IMAGE):
                    time.sleep(random.uniform(1,4))

                # Video or image tweets can also have text. Pause and read
                if (bot.tweet.type == TEXT):
                        wordcount = len(bot.tweet.text.split())
                        min_time = wordcount / 5
                        max_time = wordcount / 10
                        time.sleep(random.uniform(min_time, max_time))
                
                # Decide whether to like it
                if (random.uniform(0, 1) < 0.25):
                    print("Like")
                    if (random.uniform(0, 1) < 0.1):
                        print("Reply")
                    if (random.uniform(0, 1) < 0.1):
                        print("retweet")
                
                          
                
        
        