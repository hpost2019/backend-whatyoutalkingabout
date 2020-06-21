import tweepy
import csv
import ssl
import time
import requests


consumer_key = "YHe4bNHnfbmlmGadqPwbc5Srx"
consumer_secret = "yph8kAuAUSUr3A3ZMYz9ePoLNrumrRsuySipzVAv6J9iwxptYF"
access_key = "1186688700672905216-gzDSMDolafPu9D06aiXsQ2zEFDMNRe"
access_secret = "PXRuI3uQTRRmTdGlBdhWRplqAk8aXZXDjr1lsV5GMnGuT"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)

api = tweepy.API(auth)
keywords = []


class MyStreamListner(tweepy.StreamListener):

    def on_status(self, status):
        try:
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
            matches = []
            for word in keywords:
                if word.lower() in tweet.lower():
                    matches.extend([word])
            keywords_in_tweet = ", ".join(str(w) for w in matches)
            tweet_user = status.author.screen_name
            tweet_time = status.created_at
            tweet_source = status.source
            tweet_id = status.id

            writer.writerow([tweet, keywords_in_tweet, tweet_time,
                             tweet_user, tweet_source, tweet_id])
        except Exception as e:
            print('Encountered problem:', e)
            pass



