import sys
import re
# from retrievetrainingdata import buidTrainingSet as build_training
from retrievetrainingdata import load_training_data
from gathertweets import get_tweets
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
nltk.download('punkt')

word_features = []


class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english')
                              + list(punctuation)
                              + ['AT_USER', 'URL'])

    def process_tweets(self, tweets_list):
        processed_tweets = []
        for tweet in tweets_list:
            processed_tweets.append((self._process_tweet(tweet["text"]),
                                    tweet["label"]))
        return processed_tweets

    def _process_tweet(self, tweet):
        tweet = tweet.lower()
        tweet = re.sub(r'((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
        tweet = re.sub(r'@[^\s]+', 'AT_USER', tweet)
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
        tweet = word_tokenize(tweet)
        return [word for word in tweet if word not in self._stopwords]


def build_vocabulary(preprocessed_data):
    all_words = []
    for (words, sentiment) in preprocessed_data:
        all_words.extend(words)
    words_list = nltk.FreqDist(all_words)
    word_features = words_list.keys()
    return word_features


def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features


def main():
    tweet_processor = PreProcessTweets()
    global word_features
    search_list = []
    search_term = input("Enter the topic you want to search for: ")
    search_list.append(search_term)
    # print(search_list)
    # training_data = build_training("corpus.csv", "tweetDataFile.csv")
    training_tweets = load_training_data("tweetDataFile.csv")
    test_tweets = get_tweets(search_list)
    preproc_training_tweets = tweet_processor.process_tweets(
                                                            training_tweets)
    preprocessed_test_tweets = tweet_processor.process_tweets(test_tweets)
    word_features = build_vocabulary(preproc_training_tweets)
    training_features = nltk.classify.apply_features(extract_features,
                                                     preproc_training_tweets)
    NBayesClassifier = nltk.NaiveBayesClassifier.train(training_features)
    NBayesClassifier.show_most_informative_features(15)
    extracted_test_tweets = nltk.classify.apply_features(extract_features,
                                                         preprocessed_test_tweets)
    
    print("NBayes Classifier accuracy percent: ",
          nltk.classify.accuracy(NBayesClassifier, extracted_test_tweets))
    NBResultLabels = [NBayesClassifier.classify(extract_features(tweet[0]))
                      for tweet in preprocessed_test_tweets]

    if NBResultLabels.count('positive') > NBResultLabels.count('negative'):
        print("Overall Positive Sentiment")
        print("Positive Sentiment Percentage = "
              + str(100*NBResultLabels.count('positive')/len(NBResultLabels))
              + "%")
    else:
        print("Overall Negative Sentiment")
        print("Negative Sentiment Percentage = "
              + str(100*NBResultLabels.count('negative')/len(NBResultLabels))
              + "%")
    # print(test_tweets)
    pass


if __name__ == '__main__':
    main()
