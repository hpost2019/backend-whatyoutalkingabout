import tweepy
from dotenv import load_dotenv
import os
load_dotenv()


auth = tweepy.OAuthHandler(os.environ['CONSUMER_KEY'],
                           os.environ['CONSUMER_SECRET'])
auth.set_access_token(os.environ['ACCESS_KEY'], os.environ['ACCESS_SECRET'])

api = tweepy.API(auth)

tweets = []


class MyStreamListner(tweepy.StreamListener):
    tweet_counter = 0

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_status(self, status):
        try:
            MyStreamListner.tweet_counter += 1
            tweet_obj = status
            if 'extended_tweet' in tweet_obj._json:
                tweet = tweet_obj.extended_tweet['full_text']
            else:
                tweet = tweet_obj.text

            '''Replaces all named and numeric character
            references with Unicode characters'''
            tweet = (tweet.replace('&amp;', '&')
                     .replace('&lt;', '<')
                     .replace('&gt;', '>')
                     .replace('&quot;', '"')
                     .replace('&#39;', "'")
                     .replace(';', " ")
                     .replace(r'\u', " "))
            # print(tweet)
            tweet_dict = {"text": tweet, "label": None}
            tweets.append(tweet_dict.copy())
            if MyStreamListner.tweet_counter < 101:
                print('tweet captured: ', MyStreamListner.tweet_counter)
                return True
            else:
                return False
        except Exception as e:
            print('Encountered problem:', e)
            pass


def get_tweets(terms):
    streamingAPI = tweepy.streaming.Stream(auth, MyStreamListner())
    streamingAPI.filter(track=terms)

    return tweets
