import time
import random
from bot import TwitterBot
from constants import VIDEO, IMAGE, TEXT, SESSION_LENGTH_RANGE, GLANCE_LENGTH_RANGE, READING_TWEET_PROB, LIKE_PROB, RETWEET_PROB, REPLY_PROB, IMAGE_ENGAGEMENT_TIME_RANGE, TEXT_ENGAGEMENT_TIME_FACTOR_MIN, TEXT_ENGAGEMENT_TIME_FACTOR_MIN


bot = TwitterBot()

start_time = time.time()
print(SESSION_LENGTH_RANGE)
session_length = random.uniform(*SESSION_LENGTH_RANGE)
end_time = start_time + session_length

seconds_per_minute = 60
session_minutes = int(session_length // seconds_per_minute)
session_seconds = int(session_length % seconds_per_minute)
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
        time.sleep(random.uniform(*GLANCE_LENGTH_RANGE))
        tweets_seen += 1

        # Chance of "reading" the tweet
        if random.random() < READING_TWEET_PROB:
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
                    seconds = int(bot.tweet.seconds) + int(bot.tweet.minutes) * seconds_per_minute
              
                    quarter_video = 0.25 * seconds
                    time.sleep(random.uniform(quarter_video, seconds))
                elif (bot.tweet.type == IMAGE):
                    time.sleep(random.uniform(*IMAGE_ENGAGEMENT_TIME_RANGE))

                # Video or image tweets can also have text. Pause and read
                if (bot.tweet.type == TEXT):
                        wordcount = len(bot.tweet.text.split())
                        min_time = wordcount / TEXT_ENGAGEMENT_TIME_FACTOR_MIN
                        max_time = wordcount / TEXT_ENGAGEMENT_TIME_FACTOR_MIN
                        time.sleep(random.uniform(min_time, max_time))
                
                # Decide whether to like it
                if (random.random() < LIKE_PROB):
                    bot.like()
                    tweets_liked += 1
                    if (random.random() < RETWEET_PROB):
                        bot.reply(response.strip())
                        replies_authored += 1
                    if (random.random() < REPLY_PROB):
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
                
        
        