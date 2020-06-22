import twitter
from dotenv import load_dotenv
import os
load_dotenv()

# initialize api instance
twitter_api = twitter.Api(consumer_key=os.environ['CONSUMER_KEY'],
                          consumer_secret=os.environ['CONSUMER_SECRET'],
                          access_token_key=os.environ['ACCESS_KEY'],
                          access_token_secret=os.environ['ACCESS_SECRET'])

print(twitter_api.VerifyCredentials())


def buidTrainingSet(corpusFile, tweetDataFile):
    import csv
    import time

    corpus = []

    with open(corpusFile, 'r') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({"tweet_id": row[2],
                           "label": row[1],
                           "topic": row[0]})

    rate_limit = 180
    sleep_time = 900/180

    trainingDataSet = []
    rate_counter = 0
    for tweet in corpus:
        try:
            if rate_counter < rate_limit:
                status = twitter_api.GetStatus(tweet["tweet_id"])
                print("Tweet fetched" + status.text)
                tweet["text"] = status.text
                trainingDataSet.append(tweet)
                rate_counter += 1
            else:
                time.sleep(sleep_time)
        except EnvironmentError as e:
            print(e)
            continue
    # now we write them to the empty CSV file
    with open(tweetDataFile, 'w') as csvfile:
        linewriter = csv.writer(csvfile, delimiter=',', quotechar="\"")
        for tweet in trainingDataSet:
            try:
                linewriter.writerow([tweet["tweet_id"],
                                    tweet["text"],
                                    tweet["label"],
                                    tweet["topic"]])
            except Exception as e:
                print(e)
    return trainingDataSet


def load_training_data(file):
    import csv
    tweets = []
    with open(file) as f:
        reader = csv.reader(f)
        for row in reader:
            temp_dict = {'text': row[1], 'label': row[2]}
            tweets.append(temp_dict.copy())
        # for line in f:
        #     tweet_data = line.split(',')
        #     print(len(tweet_data))
        #     temp_dict = {'text': tweet_data[1], 'label': tweet_data[2]}
        #     tweets.append(temp_dict.copy())
    return tweets
