import time
import random
from bot import TwitterBot
from constants import VIDEO, IMAGE, TEXT


bot = TwitterBot()

start_time = time.time()
session_length = random.uniform(3*60, 15*60)
end_time = start_time + session_length

session_minutes = int(session_length // 60)
session_seconds = int(session_length % 60)
print(f'Starting a session of length {session_minutes}:{session_seconds}')

tweets_liked = 0
tweets_retweeted = 0
replies_authored = 0

tweets_seen = 0
tweets_read = 0
tweets_engaged = 0

while(time.time() < end_time):
    if bot.scroll() == 0:
        # Glance at tweet, decide whether to engage
        time.sleep(random.uniform(0,2))
        tweets_seen = 0

        # Chance of "reading" the tweet
        if random.uniform(0, 1) < 0.5:
            tweets_read += 1

            # Read the tweet
            response = None
            if (bot.tweet.type == VIDEO or bot.tweet.type == IMAGE):
                bot.download()
                response = bot.readTweet(image=True)
            else: 
                response = bot.readTweet(image=False)
            
            # This is something we want to engage in
            if (response.strip() != "No."):
                tweets_engaged += 1

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
                if (random.uniform(0, 1) < 0.75):
                    bot.like()
                    tweets_liked += 1
                    if (random.uniform(0, 1) < 0.2):
                        bot.reply(response.strip())
                        replies_authored += 1
                    if (random.uniform(0, 1) < 0.2):
                        bot.retweet()
                        tweets_retweeted += 1
                
print(f'''
End of session statistics: 
Tweets seen: {tweets_seen}
Tweets read: {tweets_read}
Tweet engagements: {tweets_engaged}
Tweets liked: {tweets_liked}
Tweets retweeted: {tweets_retweeted}
Tweets replied to: {replies_authored}
''')
                
        
        